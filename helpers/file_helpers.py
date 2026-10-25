def load_sql(cursor, file_path, params):
    with open(file_path, "r", encoding="utf-8") as file:
        sql_query = file.read()

    created_ids_and_names = []

    # Для каждой записи выполняем запрос отдельно
    for data_tuple in params:
        cursor.execute(sql_query, data_tuple)
        result = cursor.fetchone()
        created_ids_and_names.append(result)

    return created_ids_and_names