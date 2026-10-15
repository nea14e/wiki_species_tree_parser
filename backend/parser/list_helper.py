def find_index_by_condition(condition, list_with_data: list):
    for index, row in enumerate(list_with_data):
        if condition(row):
            return index
    return -1