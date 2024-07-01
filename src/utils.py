import psycopg2
import dotenv
import os
from src.api_requests import HHParser

dotenv.load_dotenv()


def create_database(db_name):
    """
    Создает новую базу данных с указанным именем. Если база данных с таким именем уже существует, она будет удалена.

    :param db_name: Имя базы данных.
    """
    conn = psycopg2.connect(dbname="postgres", user=os.getenv("user"),
                            password=os.getenv("password"), host=os.getenv("host"),
                            port=os.getenv("port"))
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_tables(db_name):
    """
    Создает таблицы employers и vacancies в указанной базе данных.

    :param db_name: Имя базы данных.
    """
    conn = psycopg2.connect(dbname=db_name, user=os.getenv("user"),
                            password=os.getenv("password"), host=os.getenv("host"),
                            port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
            )
            """)

            cur.execute("""CREATE TABLE vacancies (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        url VARCHAR(255),
                        salary_from INTEGER,
                        salary_to INTEGER,
                        employer INTEGER REFERENCES employers(id),
                        area VARCHAR(100)
                        )
                        """)
    conn.close()


def insert_tables(db_name):
    """
    Заполняет таблицы employers и vacancies данными, полученными с сайта hh.ru.

    :param db_name: Имя базы данных.
    """
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.get_all_vacancies()
    conn = psycopg2.connect(dbname=db_name, user=os.getenv("user"),
                            password=os.getenv("password"), host=os.getenv("host"),
                            port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("""INSERT INTO employers VALUES (%s, %s)""",
                            (employer["id"], employer["name"]))
            for vacancy in vacancies:
                cur.execute("""INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s) 
                                     ON CONFLICT (id) DO NOTHING""",
                            (vacancy["id"], vacancy["name"], vacancy["url"], vacancy["salary_from"],
                             vacancy["salary_to"], vacancy["employer"], vacancy["area"]))
    conn.close()


def delete_database(db_name):
    """
    Удаляет базу данных с указанным именем.(Чтобы не создавалось масса баз данных)
    """
    conn = psycopg2.connect(dbname="postgres", user=os.getenv("user"),
                            password=os.getenv("password"), host=os.getenv("host"),
                            port=os.getenv("port"))
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")

    cur.close()
    conn.close()
