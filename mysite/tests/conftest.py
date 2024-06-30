import pytest
from rest_framework.test import APIClient

from django.core.management import call_command


@pytest.fixture(scope="session", autouse=True)
def setup_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # Создайте базу данных и примените миграции
        call_command("migrate")

        # Заполните базу данных тестовыми данными
        call_command("loaddata", "test_data.json")

    yield

    with django_db_blocker.unblock():
        # Очистите базу данных после завершения всех тестов
        call_command("flush", "--noinput")


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def auth_client(): ...
