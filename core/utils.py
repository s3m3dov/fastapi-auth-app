import json


def json_prettify(json_dict):
    return json.loads(
        json.dumps(
            json_dict,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")
    )
