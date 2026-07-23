import os

import psycopg2


def get_db_connection() -> psycopg2.extensions.connection:
    """
    Create and return a new PostgreSQL connection using environment variables.
    """
    host = os.getenv("DATABASE_HOSTNAME")
    port = os.getenv("DATABASE_PORT")
    name = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")

    if not all([host, port, name, user, password]):
        raise RuntimeError(
            "Database environment variables are not fully configured. "
            "Expected DATABASE_HOSTNAME, DATABASE_PORT, DATABASE_NAME, "
            "DATABASE_USERNAME, DATABASE_PASSWORD."
        )

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=name,
        user=user,
        password=password,
    )

