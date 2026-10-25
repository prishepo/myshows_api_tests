from http import HTTPStatus

import allure
import pytest

from config.api_config import BASE_URL


@allure.suite("Тесты на эндпоинт /series")
class TestGetSeries:
    @pytest.mark.series_tests
    @allure.title("Получение списка сериалов: успешный сценарий")
    def test__get_series(self, api_session, create_and_del_series):

        payload = {'sort': 'id_desc'}
        with allure.step("Получение списка сериалов"):
            response = api_session.get(BASE_URL + '/series', params=payload)
            body = response.json()
            assert response.status_code == HTTPStatus.OK
            for i in create_and_del_series:
                series_in_list = False
                for x in body:
                    if i['id'] == x['id'] and i['name'] == x['name']:
                        series_in_list = True
                        break
                assert series_in_list == True
