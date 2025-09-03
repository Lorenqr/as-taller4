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
client = MongoClient(settings.AUTH_DB_URL)
db = client["auth_db"]
users_collection = db["users"]

# Crear índice único para email
try:
    users_collection.create_index("email", unique=True)
except errors.PyMongoError as e:
    print(f"[WARN] No se pudo crear índice único en 'users': {e}")

# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="Auth Service", version="1.0.0")

# ----------- Modelos -----------
class User(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    role: str = "cliente"


class UserOut(BaseModel):
    email: EmailStr
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


# ----------- Utilidades -----------
VALID_ROLES = {"cliente", "vendedor", "admin"}


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(email: str):
    return users_collection.find_one({"email": email})


def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(email)
    if user is None:
        raise credentials_exception
    return {"email": user["email"], "role": role or user.get("role")}


# ----------- Endpoints -----------
@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}


@app.post("/register", response_model=UserOut, status_code=201)
def register(user: User):
    if user.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Rol inválido")

    hashed_password = get_password_hash(user.password)
    user_dict = {
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
    }

    try:
        users_collection.insert_one(user_dict)
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    return {"email": user.email, "role": user.role}


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["email"], "role": current_user["role"]}
