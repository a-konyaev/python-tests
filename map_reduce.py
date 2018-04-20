import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    key = record[1] # assign order_id from each record as key
    value = list(record) # assign whole record as value for each key
    mr.emit_intermediate(key, value) # emit key-value pairs

def reducer(key, value):
    for index in range (1, len(value)):
        mr.emit(value[0] + value[index])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)