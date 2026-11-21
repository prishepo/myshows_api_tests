import allure

import psycopg
from helpers.file_helpers import load_sql
from psycopg.rows import dict_row
import pytest
import requests
import os

conn_params = {
    "dbname": os.getenv("DB_NAME", "my-shows-rating"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432"))
}

@pytest.fixture(scope="session")
def api_session():
    with allure.step("Инициализация api session"):
        with requests.Session() as my_show_session:
            my_show_session.headers.update()
            yield my_show_session


@pytest.fixture()
def create_one_series():
    conn = psycopg.connect(**conn_params, row_factory=dict_row)
    try:
        with allure.step("Добавление сериалов в БД"):
            with conn.cursor() as cur:
                added_series_result = load_sql(cur, "data/my_show_INSERT_1_series.sql")
                conn.commit()
        yield added_series_result,conn
        with allure.step("Удаленые добавленного сериала из БД"):
            id = added_series_result[0]['id']
            with conn.cursor() as cur:
                cur.execute("""DELETE FROM public.series
                                 WHERE id=%s""", (id,))
                conn.commit()
    finally:
        conn.close()

@pytest.fixture()
def create_and_del_series(request):
    if hasattr(request, "param"):
        sql_file_path = request.param
    else:
        sql_file_path = "data/my_show_INSERT.sql"

    conn = psycopg.connect(**conn_params, row_factory=dict_row)
    try:
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM public.series""")
            conn.commit()
        if not sql_file_path:
            yield 0
        else:
            with allure.step("Добавление сериалов в БД"):
                with conn.cursor() as cur:
                    added_series_result = load_sql(cur, sql_file_path)
                    conn.commit()
            yield len(added_series_result)
        with allure.step("Очистка БД"):
            with conn.cursor() as cur:
                cur.execute("""DELETE FROM public.series""")
                conn.commit()
    finally:
        conn.close()




