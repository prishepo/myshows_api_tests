import yaml
from pathlib import Path


def load_sql(cursor, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        sql_query = file.read()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return result


def load_yaml(filename: str) -> dict:
    path = Path(__file__).parent.parent / "data" / filename
    with path.open(mode="r", encoding="utf-8") as file:
        return yaml.safe_load(file)