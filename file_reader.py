import sys


class FileReader:
    def __init__(self, path):
        self._path = path

    def read(self):
        try:
            with open(self._path, 'r') as f:
                return f.read()
        except IOError:
            return ""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("")
        exit(0)

    path = sys.argv[1]
    reader = FileReader(path)
    print(reader.read())