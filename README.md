# Taller #4 de Arquitectura de Software: Microservicios

Este proyecto proporciona una plantilla para la implementación de un sistema con arquitectura de Microservicios, utilizando Python y Contenedores.

## Objetivos del Taller

* Diseñar microservicios independientes que se comunican entre sí.
* Implementar API RESTful con FastAPI.
* Utilizar diferentes tipos de bases de datos para cada microservicio.
* Implementar un front-end básico para hacer uso de los microservicios.
* Contenerizar aplicaciones con Docker.
* Orquestar la infraestructura con Docker Compose.

## Elige un Tema

Cada estudiante debe elegir uno de los siguientes temas para desarrollar sus microservicios. El Taller #4 consiste en completar el esqueleto del repositorio base, implementando la lógica de los servicios que se indican en tu tema.

### 1. Sistema de Gestión de Biblioteca Universitaria

Este proyecto propone una plataforma digital para la administración integral de una biblioteca universitaria, donde estudiantes, profesores y administradores puedan interactuar de forma eficiente. El sistema incluye un módulo de **autenticación** que gestiona los roles y permisos de cada usuario; un microservicio de **catálogo** que centraliza la información de libros, autores y categorías; un microservicio de **préstamos** que controla la gestión de préstamos, devoluciones y multas; y finalmente un microservicio de **reservas** que permite a los usuarios apartar libros de manera anticipada y recibir notificaciones oportunas. La combinación de PostgreSQL, MongoDB y Redis asegura una gestión robusta y rápida de la información.

### 2. Plataforma de Reservas de Restaurante

Este sistema busca digitalizar la experiencia de reservar mesas en restaurantes, permitiendo que los usuarios puedan registrarse, explorar opciones y visualizar menús en línea. A través de un microservicio de **autenticación**, se gestiona el acceso de usuarios y restaurantes; el microservicio de **restaurantes** organiza la información de locales, mesas y horarios; el microservicio de **reservas** administra la disponibilidad y confirma espacios en tiempo real; y el microservicio de **menús** centraliza la información de platos, categorías y precios. La combinación de PostgreSQL y MongoDB optimiza la gestión de datos estructurados y transaccionales, mientras que Redis garantiza rapidez en el acceso a disponibilidad.

### 3. E-commerce de Productos Artesanales

Este proyecto plantea un **marketplace especializado en artesanías**, donde artesanos pueden ofrecer directamente sus productos a clientes interesados, eliminando intermediarios y potenciando la economía local. El microservicio de **autenticación** permite distinguir entre clientes y vendedores; el microservicio de **productos** organiza los catálogos, categorías y valoraciones; el microservicio de **pedidos** gestiona el proceso completo de compra con diferentes estados; y el microservicio de **pagos** asegura la integración con pasarelas y métodos de pago confiables. La combinación de bases de datos orientadas a documentos y relacionales facilita tanto la flexibilidad del catálogo como la seguridad de las transacciones.

### 4. Sistema de Gestión de Proyectos

Este proyecto consiste en una plataforma colaborativa que facilita la planificación y ejecución de proyectos en equipos multidisciplinarios. Incluye un microservicio de **autenticación** para el registro de usuarios y conformación de equipos; un microservicio de **proyectos** donde se configuran los objetivos, plazos y responsables; un microservicio de **tareas** que gestiona asignaciones, estados y dependencias; y un microservicio de **documentos** que permite almacenar, versionar y compartir archivos entre los miembros del equipo. La infraestructura combina PostgreSQL para la gestión estructurada de proyectos, MongoDB para las tareas dinámicas y GridFS para documentos, garantizando un entorno ágil y escalable.

### 5. Aplicación de Delivery de Comida

Este proyecto busca digitalizar el proceso de pedidos de comida a domicilio, conectando a clientes con restaurantes y repartidores en tiempo real. El microservicio de **autenticación** permite registrar y gestionar los diferentes actores (clientes, restaurantes y repartidores); el microservicio de **restaurantes** organiza menús, establecimientos y horarios de atención; el microservicio de **pedidos** centraliza la creación, confirmación y seguimiento de órdenes; y el microservicio de **repartidores** gestiona la logística de entregas, incluyendo ubicación y disponibilidad. La combinación de PostgreSQL, MongoDB y Redis asegura rapidez en búsquedas, confiabilidad en las transacciones y eficiencia en el seguimiento de las entregas.

### 6. Sistema de Reservas de Vuelos

Este sistema está diseñado como una plataforma para que usuarios puedan buscar, reservar y pagar vuelos de manera sencilla, integrando aerolíneas y usuarios en un solo entorno digital. El microservicio de **autenticación** gestiona la relación entre viajeros y aerolíneas; el microservicio de **vuelos** administra información de horarios, rutas, aeronaves y disponibilidad de asientos; el microservicio de **reservas** coordina el proceso de compra, check-in y generación de tiquetes electrónicos; y el microservicio de **pagos** asegura la facturación y gestión de transacciones. El uso de PostgreSQL y MongoDB garantiza estabilidad para la información estructurada y flexibilidad para la gestión de reservas dinámicas.

### 7. Red Social para Deportistas

Este proyecto plantea una red social enfocada en atletas y entusiastas del deporte, que permite compartir logros, registrar actividades y conectar con otros usuarios. El microservicio de **autenticación** gestiona usuarios individuales y clubes; el microservicio de **actividades** centraliza el registro de entrenamientos y logros deportivos; el microservicio **social** permite seguir usuarios, interactuar mediante comentarios y mensajes, y mantener la actividad en tiempo real; y el microservicio de **eventos** organiza competiciones, torneos y encuentros. Con MongoDB, Redis y PostgreSQL, la plataforma equilibra la gestión dinámica de interacciones sociales con la organización formal de eventos deportivos.

### 8. Plataforma de Cursos Online

Este proyecto propone un sistema de aprendizaje digital que conecta estudiantes e instructores, ofreciendo cursos, contenidos multimedia y seguimiento de progreso. El microservicio de **autenticación** organiza perfiles de estudiantes e instructores; el microservicio de **cursos** gestiona programas, módulos y lecciones; el microservicio de **progreso** rastrea el avance de cada estudiante mediante métricas personalizadas; y el microservicio de **evaluaciones** aplica cuestionarios y calificaciones de forma automática. La combinación de PostgreSQL y MongoDB permite manejar contenidos estructurados y flexibles, garantizando al mismo tiempo un seguimiento confiable del desempeño académico.

### 9. Sistema de Monitoreo de Salud

Este proyecto consiste en una aplicación para que usuarios puedan registrar, analizar y visualizar métricas de salud, conectando datos con profesionales médicos cuando sea necesario. El microservicio de **autenticación** organiza perfiles de usuarios y profesionales de la salud; el microservicio de **métricas** permite ingresar datos como presión arterial, ritmo cardiaco o peso; el microservicio de **análisis** procesa esta información y genera gráficos y tendencias; y el microservicio de **alertas** envía notificaciones preventivas y recordatorios personalizados. PostgreSQL, MongoDB y Redis permiten un balance óptimo entre almacenamiento histórico, flexibilidad de métricas y rapidez en alertas.

### 10. Mercado de Second-Hand

Este proyecto plantea una plataforma digital para la compra y venta de productos de segunda mano, enfocada en la confianza entre compradores y vendedores. El microservicio de **autenticación** gestiona perfiles de usuarios, diferenciando compradores y vendedores; el microservicio de **productos** organiza listados y categorías; el microservicio de **transacciones** administra el proceso de compra-venta y el envío de productos; y el microservicio de **valoraciones** refuerza la reputación de los usuarios a través de comentarios y calificaciones. El uso de MongoDB y PostgreSQL asegura la flexibilidad necesaria para gestionar publicaciones variadas, junto con la estabilidad y seguridad que requieren las transacciones comerciales.

## Proceso de Desarrollo

Sigue estos pasos para comenzar tu proyecto:

1. Clonar el repositorio base:

    ```bash
    git clone https://github.com/UR-CC/as-taller4.git
    cd as-taller4
    ```

2. Configuración inicial:

    Crea el archivo de variables de entorno a partir del ejemplo.

    ```bash
    cp .env.example .env
    ```

    **Nota**: Asegúrate de configurar las variables de entorno en el archivo `.env` si es necesario.

3. Familiarízate con la estructura del proyecto:
    
    * `frontend/`: La aplicación web principal (Flask).
    * `api-gateway/`: El enrutador de peticiones (FastAPI).
    * `services/`: Directorio donde desarrollarás tus microservicios (FastAPI).

    **Nota**: Hay comentarios `# TODO` que brindan indicaciones de lo que debe implementarse.

4. Selecciona uno de los temas propuestos.

5. Renombra los directorios de los microservicios `service[123]` según tu tema en la carpeta `services/`.

6. Revisa los archivos `main.py`, `Dockerfile`, y `requirements.txt` para cada uno de los microservicios.

7. Ajusta el archivo `docker-compose.yml` de tal forma que los servicios y bases de datos coincidan con tu tema.

8. Implementa la lógica de cada microservicio siguiendo los requisitos de tu tema.

    * Define e implementa tu modelo de datos.
    * Crea los endpoints de las API.
    * Implementa la comunicación entre servicios.
    * Conecta cada servicio a su base de datos.

### Ejecutar el Proyecto

Una vez que tengas tus servicios configurados, puedes levantar todo el stack con un solo comando:

```bash
docker-compose up --build
```

Esto construirá las imágenes y ejecutará todos los contenedores. Podrás acceder al frontend en `http://localhost:5000` y al API Gateway en `http://localhost:8000`.

