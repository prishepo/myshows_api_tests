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
def create_and_del_series():
    conn = psycopg.connect(**conn_params, row_factory=dict_row)
    try:
        with allure.step("Добавление сериалов в БД"):
            data = [('Дикий ангел', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/1898899/20df477e-8a1c-4cf3-8518-7873e196ab60/300x450', 1,
                     'will_watch', None),
                    ('Время приключений', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/1704946/8997def3-7896-48c4-85db-b600eca3f983/300x450', 1,
                     'watching', None),
                    ('Джентльмены', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/10812607/b63d7300-204d-42a9-a3f8-49c02c462011/300x450', 1,
                     'watching', None)]
            with conn.cursor() as cur:
                added_series_result = load_sql(cur, "data/my_show_INSERT.sql", data)
                conn.commit()
        yield added_series_result
        with allure.step("Удаленые добавленных сериалов из БД"):
            list_of_ids = [x['id'] for x in added_series_result]
            with conn.cursor() as cur:
                cur.execute("""DELETE FROM public.series
                                 WHERE id IN (%s, %s, %s)""", (list_of_ids[0],list_of_ids[1],list_of_ids[2]))
                conn.commit()
    finally:
        conn.close()



