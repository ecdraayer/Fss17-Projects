import sys
import re

def isBad( n ):
  return (len(n) < NumofAttributes or len(n) > NumofAttributes)

def removeJunk( line ):
  line = str(line)
  line = re.sub(re.compile("#.*?\n" ) ,"" ,line)
  return (line.replace(" ", "")).rstrip()

def is_number( s ):
  try: 
    float(s)
    return True
  except ValueError:
    return False

row1 = True
IgnoreList = []

csvFileName = sys.argv[1]
NumofAttributes = 0
Data = []

with open(csvFileName) as f:
  row = []

  for line in f:
    if row1:
      line = removeJunk(line)
      headers = line.split(',')

      NumofAttributes = len(headers)

      for x in range(0,NumofAttributes):
        if headers[x][0] == '?':
          IgnoreList.append(x)
        else:
          row.append(headers[x])
      
      Data.append(row)
      row = []
      row1 = False
    else:
      line = removeJunk(line)
      if line[-1] == ',':
        line = str(line) + str(next(f))

      values = line.split(',')

      if isBad( values ):
         print "Bad Number of Values"
         continue

      for x in range(0, len(values)):

        if ( x in IgnoreList ):
          continue

        if ( is_number(values[x]) ):
          row.append(float(values[x])) 
        else:
          row.append(values[x])
      
      
      Data.append(row)
      row = []

print Data




