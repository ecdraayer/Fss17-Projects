import sys
import re
import time

class Table(object):
  def __init__(self):
    self.headers = None
    self.rows = []    
    self.goals = 0     
  
  def addHeaders(self, inp):
    self.headers = inp
    #self.headers.append(inp)
   
  def addData(self, inp):
    self.rows.append(inp)

  def __str__(self):
    result = ""
    for x in self.headers:
      result += x.name + " "
    
    result += "\n"
    for x in self.rows:
      result += str(x) + '\n'


    return result
  
  def updateHeaders(self, row):
    i = 0
    for x in self.headers:
      if(x.max == -1 and x.min == -1):
        x.max, x.min = row[i], row[i]
      else:
        if(x.max < row[i]):
          x.max = row[i]

        if(x.min > row[i]):
          x.min = row[i]
      i += 1


class Row(object):
  def __init__(self):
    self.data = []
    self.index = -1
    self.rank = -1

  def __str__(self):
    return "cells=%s, id=%d" %(str(self.data), self.index)


class Header(object):
  def __init__(self):
    self.name = ""
    self.position = -1
    self.dataType = ""
    self.type = ""
    self.goal = False
    self.goals = 0
    self.weight = 0
    self.max = -1
    self.min = -1
    self.std = 0
    self.mean = 0
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

# Normalizes the current data value v
def normalize(v, minv, maxv):
  return (v - minv) / ((maxv-minv) + (10**-2))
    
def dominate1(r1, r2, hs):
  e = 2.71828
  sum1,sum2 = 0.0,0.0
  n = 0
  for h in hs:
    if(h.goal == True):
      n += 1

  for h in hs:
    if (h.goal == False):
      continue
    w = h.weight
    x = normalize(r1[h.position], h.min, h.max)
    y = normalize(r2[h.position], h.min, h.max)
    sum1 = sum1 - e**(w * (x-y)/n)
    sum2 = sum2 - e**(w * (y-x)/n)

  return sum1/n < sum2/n

def dominate(row, t, indx):
  rank = 0
  for i, value in enumerate(t.rows):
    if i != indx:
      if dominate1(row.data, value.data, t.headers):
        rank += 1


  return rank


# Test if a row of data is less than or greater than the number of attributes recorded
def isBad(n, NumofAttributes):
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
def checktype( value, i, T ):
  if is_number(value):
    if((T.headers[i]).dataType == "num"):
      return True
    else:
      return False
  else:
    if((T.headers[i]).dataType == "sym"):
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
      h.dataType = "sym"
    else:
      h.type = "independent"
      h.dataType = "num"

    


def main():
  # Start the timer
  start_time = time.time()
  isHeader = True
  csvFileName = sys.argv[1]
  IgnoreList = []
  T = Table()
  ind = 0
  num = 0
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

        T.addHeaders(row)

        isHeader = False
        Line_Num += 1
        num += 1

      else:
        r = Row()
        r.index = num-1 + 1795
        num += 1
        if line[-2] == ',':
          line = incomplete(line, f)
     
        line = removeJunk(line)
        values = mysplit(line, ',')

        if isBad( values, NumofAttributes ):
          print "ERROR: Bad Number of Values on Line " + str(Line_Num)
          continue

        for x in range(len(values)):
          if ( x in IgnoreList ):
            continue
        
          if (checktype(values[x], x, T) == False):
            print "ERROR: Bad Data Type on line " + str(Line_Num) + ", col " + str(x)
            break

          if ( is_number(values[x]) ):
            row.append(float(values[x])) 
          else:
            row.append(values[x])
      
          if (len(row) == NumofAttributes-len(IgnoreList)):
            Line_Num += 1
            r.data = row
            T.addData(r)
            T.updateHeaders(row)
  

  for i, row in enumerate(T.rows):
    row.rank = dominate(row, T, i)
  
  sort = sorted(T.rows, key=lambda row: -row.rank)
  for h in T.headers:
    print h.name+",",

  print
  for i in range(5):
    print (sort[i])

  print

  for i in range(-6, 0):
    print (sort[i])
 




if __name__ == "__main__":
  main()

