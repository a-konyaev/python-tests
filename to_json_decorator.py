from functools import wraps
import json


def to_json(func):
    @wraps(func)
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        return json.dumps(res)
    return inner


@to_json
def get_data(x, d):
    d0 = {
        'data': 42,
        'x': x
    }
    return {**d0, **d}


print(get_data(111, {'qqq': 123}))
