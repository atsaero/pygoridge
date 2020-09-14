import datetime
import json


def default(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    else:
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")


def json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False, default=default)


def json_loads(s):
    return json.loads(s)
