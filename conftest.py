from dotenv import load_dotenv
import subprocess

load_dotenv()
pytest_plugins = ['fixtures.api_fixtures']


def pytest_addoption(parser):
    parser.addoption(
        "--html-report",
        action="store_true",
        default=False,
        help="Сгенерировать отчёт в формате HTML в директорию allure-report",
    )

def pytest_sessionfinish(session):
    if session.config.getoption("--html-report"):
        subprocess.call(["allure", "generate", "--clean", "--single-file", "allure-results"], shell=True)
