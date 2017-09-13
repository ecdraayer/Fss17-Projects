import sys
import re
import time

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

def incomplete(line, f):
  try:
    line = str(line) + str(next(f))
  except:
    line = line
  return line

def mysplit(s, delim=None):
  return [x for x in s.split(delim) if x]

def checktype( value, i ):
  if is_number(value):
    if(('$' in headers[i][0]) or ('<' in headers[i][0]) or('>' in headers[i][0])):
      return True
    else:
      return False
  else:
    if(headers[i][0].isalpha()):
      return True
    else:
      return False


start_time = time.time()
row1 = True
IgnoreList = []

csvFileName = sys.argv[1]
NumofAttributes = 0
headers = []
Data = []

with open(csvFileName) as f:
  Line_Num = 1
  for line in f:
    row = []

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
      row1 = False
      Line_Num += 1
    else:
      if line[-2] == ',':
        line = incomplete(line, f)
        Line_Num += 1
     
      line = removeJunk(line)
      values = mysplit(line, ',')

      if isBad( values ):
         print "ERROR: Bad Number of Values on Line " + str(Line_Num)
         continue

      for x in range(0, len(values)):

        if ( x in IgnoreList ):
          continue
        
        if (checktype(values[x], x) == False):
           print "ERROR: Bad Data Type on line " + str(Line_Num) + ", col " + str(x)
           break

        if ( is_number(values[x]) ):
          row.append(float(values[x])) 
        else:
          row.append(values[x])
      
      Line_Num += 1
      if (len(row) == NumofAttributes-len(IgnoreList)):
        Data.append(row)
#print Data
print("--- %s seconds ---" % (time.time() - start_time))


