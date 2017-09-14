import sys
import re
import time

class Table(object):
  def __init__(self):
    self.data = []
    self.goals = 0
  
  def add(self, inp):
    self.data.append(inp)

  def __str__(self):
    result = ""
    for x in self.data:
      for y in x:
        result += y.name + '\n'


    return result
    
class Header(object):
  def __init__(self):
    self.name = ""
    self.position = -1
    self.dataType = ""
    self.type = ""
    self.goal = False
    self.weight = 0
    self.std = -1
    self.mean = -1
    self.count = 0

  def __str__(self):
    result = self.name + "\n"
    result += str(self.position) + "\n"
    result += str(self.position) + "\n"
    result += str(self.dataType) + "\n"
    result += str(self.type) + "\n"
    result += str(self.goal) + "\n"
    result += str(self.weight) + "\n"
    result += str(self.std) + "\n"
    result += str(self.mean) + "\n"
    result += str(self.count) + "\n"
    return result


# Test if a row of data is less than or greater than the number of attributes recorded
def isBad(n):
  return (len(n) < NumofAttributes or len(n) > NumofAttributes)

# This function removes whitespace and anything after comment
# characters (#) that might be in a row of data we are reading
def removeJunk(line):
  line = str(line)
  line = re.sub(re.compile("#.*?\n" ) ,"" ,line)
  return (line.replace(" ", "")).rstrip()

# Test if the given input is a number, if it is, return true
def is_number(s):
  try: 
    float(s)
    return True
  except ValueError:
    return False

# Had to write my own split function because python's built in one sucks ass
def mysplit(s, delim=None):
  return [x for x in s.split(delim) if x]

# Checks what data type belongs in column i and records it
def checktype( value, i, headers ):
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

# Completes the line if it is incomplete (ends with comma)
def incomplete(line, f):
  try:
    line = str(line) + str(next(f))
  except:
    line = line
  return line


def checkSymbols( h, t ):
  if( ('<' in h.name) ):
 
    if( ('$') in h.name ):
      h.type = "independent"
    else:
      h.type = "dependent"
    t.goals += 1
    h.weight = -1
    h.goal = True
    h.dataType = "num"

  elif( ('>' in h.name) ):

    if( ('$') in h.name ):
      h.type = "independent"
    else:
      h.type = "dependent"

    t.goals += 1
    h.weight = 1
    h.goal = True
    h.dataType = "num"

  else:

    if( ('!') in h.name ):
      t.goals += 1
      h.type = "dependent"
      h.goal = True
    else:
      h.type = "independent"

    h.dataType = "sym"


def main():
  # Start the timer
  start_time = time.time()
  isHeader = True
  csvFileName = sys.argv[1]
  IgnoreList = []
  T = Table()
  dominate_dict={}

  with open(csvFileName) as f:
    Line_Num = 1

    for line in f:
      row = []

      # Check if on the first line of the csv
      if isHeader:
        line = removeJunk(line)

        # Get the name of each header
        headers = line.split(',')
 
        # Get the number of attributes (cols)
        NumofAttributes = len(headers)

        for x in range(NumofAttributes):
          h = Header()
          h.position = x
          h.name = headers[x]
          checkSymbols(h, T)
          # Check if col should be ignored (starts with '?')
          if '?' in headers[x]:
            IgnoreList.append(x)
          else:
            row.append(h)

        T.add(row)
        print T
        isHeader = False
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

        for x in len(values):

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
            T.add(row)



if __name__ == "__main__":
  main()

