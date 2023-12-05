import sqlite3
import docker


def get_docker_client():
    # Inicjalizuj klienta Dockera
    client = docker.from_env()
    return client


def create_db(container_name):
    client = get_docker_client()

    # Uruchom kontener z bazą danych SQLite w pamięci
    container = client.containers.run(
        "sqlite3",
        name=container_name,
        detach=True,
        auto_remove=True,  # Kontener zostanie usunięty po zakończeniu
    )

    # ... (reszta kodu jak wcześniej)


def connect_db(container_name):
    client = get_docker_client()

    # ... (reszta kodu jak wcześniej)


# Przykład użycia
container_name = "my_sqlite_container"
create_db(container_name)
conn = connect_db(container_name)

# Teraz możesz używać `conn` do operacji na bazie danych SQLite
