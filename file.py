import tempfile
import os


class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_for_iter = None

    def __add__(self, other):
        if other == None:
            return self

        path = os.path.join(
            tempfile.gettempdir(),
            os.path.splitext(os.path.basename(self.filepath))[0] + '_' +
            os.path.basename(other.filepath))

        sum_file = File(path)
        sum_file.write(self.read())
        sum_file.write(other.read())

        return sum_file

    def __str__(self):
        return self.filepath

    def __iter__(self):
        self.file_for_iter = open(self.filepath, 'r')
        return self

    def __next__(self):
        line = self.file_for_iter.readline()
        if line == '':
            self._close_iter()
            raise StopIteration
        return line

    def _close_iter(self):
        if self.file_for_iter is not None and not self.file_for_iter.closed:
            self.file_for_iter.close()

    def __del__(self):
        self._close_iter()

    def read(self):
        with open(self.filepath, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.filepath, 'a') as f:
            f.write(text)


# f1 = File(r'C:\.my\github\python-tests\tmp.txt')
# f1.write("111\n")
#
# f2 = File(r'C:\.my\github\python-tests\tmp2.txt')
# f2.write("222\n")
#
# f3 = f1 + f2
# print(f3)
#
# for line in f3:
#     print(line)
#
# del f3