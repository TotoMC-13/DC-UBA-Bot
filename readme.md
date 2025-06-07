## Entorno de Desarrollo

Este proyecto usa Docker y Docker Compose para gestionar los servicios. Tenes dos formas principales de trabajar:

### 1. Despliegue Completo con Docker

1.  Copia `.env.example` a `.env`.
2.  Edita `.env` y rellena todas las variables. Asegurate de que `DB_URL` apunte a `mongo-db`.
3.  Ejecuta `docker compose up -d`.

### 2. Desarrollo (Para trabajar desde el IDE)

Este método te permite ejecutar y depurar el código del bot directamente desde tu IDE (ej. VS Code) mientras la base de datos corre en un contenedor Docker.

1.  **Levanta la base de datos:**
    ```bash
    docker compose up -d mongo-db
    ```

2.  **Configura tu entorno local:**
    *   Copia `.env.example` a un nuevo archivo llamado `local.env`.
    *   Edita `local.env` y rellena los secretos.
    *   **Importante:** Asegurate de que la variable `DB_URL` en `local.env` apunte a `localhost`, no a `mongo-db`.

3.  Listo, ahora podes ejecutar y trabajar en tu archivo `main.py` desde tu IDE.