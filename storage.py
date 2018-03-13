import os
import tempfile
import argparse
import json


def storage_file_path():
    return os.path.join(tempfile.gettempdir(), 'storage.data')


def read_val(k):
    with open(storage_file_path(), 'r') as f:
        content = f.read()

    return json.loads(content).get(k)


def write_val(k, v):
    with open(storage_file_path(), 'r+') as f:
        d = json.loads(f.read())
        old = d.get(k)
        if old is None:
            d[k] = v
        else:
            d[k] = f"{old}, {v}"

        f.seek(0)
        f.write(json.dumps(d))


parser = argparse.ArgumentParser()
parser.add_argument("--key", required=True)
parser.add_argument("--val")

args = parser.parse_args()
key = args.key
val = args.val

if val is None:
    print(read_val(key))
else:
    write_val(key, val)
