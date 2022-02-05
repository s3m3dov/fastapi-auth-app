import json


def prettify_json(json_dict) -> str:
    return json.dumps(
        json_dict,
        ensure_ascii=False,
        allow_nan=False,
        indent=4,
        separators=(", ", ": "),
    )
