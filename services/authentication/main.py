from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr
from passlib.context import CryptContext
from jose import JWTError, jwt
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from typing import Optional


# Configuración común
from common.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Conexión MongoDB
client = MongoClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Modelos
class User(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utilidades
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(email: str):
    user = db.users.find_one({"email": email})
    if user:
        return UserInDB(**user)
    return None

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Endpoints
@app.get("/")
def root():
    return {"message": "Auth service funcionando"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-service"}

@app.post("/register", response_model=User)
def register(user: UserRegister):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    db.users.insert_one(user_dict)
    return User(**user_dict)

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user