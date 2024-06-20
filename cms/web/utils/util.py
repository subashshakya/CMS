from typing import List


def find_missing_fields(
    required_fields: List[str], request_fields: List[str]
) -> List[str]:
    return [field for field in required_fields if field not in request_fields]


def update_fields(db_obj: object, request_obj: object) -> object:
    return {key: request_obj[key] for key in db_obj.keys()}
