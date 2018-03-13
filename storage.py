import os
import tempfile
import argparse
import json


storage_data_path = os.path.join(tempfile.gettempdir(), 'storage.data')


def read_val(k):
    if not os.path.exists(storage_data_path):
        return None

    with open(storage_data_path, 'r') as f:
        content = f.read()

    return json.loads(content).get(k)


def write_val(k, v):
    if not os.path.exists(storage_data_path):
        with open(storage_data_path, 'w') as f:
            f.write(json.dumps({k: v}))
    
    else:
        with open(storage_data_path, 'r+') as f:
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
