from http import HTTPStatus

import allure
import pytest

from config.api_config import BASE_URL
from helpers.file_helpers import load_yaml
from jsonschema import validate


@allure.suite("Тесты на эндпоинт /series")
class TestGetSeries:
    @pytest.mark.series_tests
    @allure.title("Обновление информации о сериале: успешный сценарий")
    @pytest.mark.parametrize("param_for_json, new_value",
                             [("name", "The Office"),
                              ("photo", "https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/4716873/bcd93c26-8a5a-4457-8fab-51805b86f47e/300x450"),
                              ("rating", 10), (
                                      "status", "watched"), ("review", "Интересный сериал")],
                             ids=["change_name", "change_photo", "change_rating",
                                  "change_status", "change_review"])
    def test__put_series(self, api_session, create_one_series, param_for_json, new_value):
        series_data, conn = create_one_series
        series_id = series_data[0]['id']
        serial_data_copy = series_data[0].copy()
        serial_data_copy[param_for_json] = new_value


        with allure.step("Изменение данных о сериале"):
            response = api_session.put(BASE_URL + '/series/' + str(series_id),
                                      json=serial_data_copy
            )
            assert response.status_code == HTTPStatus.OK
        with allure.step("Проверка изменений в БД"):
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM public.series
                                 WHERE id=%s""",
                            (series_id,))
                result = cur.fetchone()
                assert result[param_for_json] == new_value



    @pytest.mark.series_tests
    @allure.title("Проверка добавления разного количества сериалов: успешные сценарии")
    @pytest.mark.parametrize("create_and_del_series",
                             ["data/my_show_INSERT_3_series.sql", "data/my_show_INSERT_1_series.sql", None],
                             ids=["add_3_series", "add_1_series", "add_0_series"],
                             indirect=True,
                             )
    def test__get_series(self, api_session, create_and_del_series):
        payload = {'sort': 'id_desc'}
        with allure.step("Получение списка сериалов"):
            response = api_session.get(BASE_URL + '/series', params=payload)
            body = response.json()
        with allure.step("Проверка кода ответа, схемы ответа и соответствия количества добавленных строк в БД"):
            template = load_yaml("series_get.yml")
            assert response.status_code == HTTPStatus.OK
            assert len(body) == create_and_del_series
            validate(body, template)
