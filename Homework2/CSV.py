import sys
import re
import time

#class table:
#  def __inti__(self, ):
class row:
  pass
  #def __init__(self):

#class col:
#  def __init__(self, ):

# This function removes whitespace and anything after comment
# characters (#) that might be in a row of data we are reading
def removeJunk(line):

def main():
  # Start the timer
  start_time = time.time()
  isHeader = True
  csvFileName = sys.argv[1]

  with open(csvFileName) as f:
    
    # Check if the info being read is the header
    if isHeader:
      line = removeJunk(line)

      # Get the name of each header
      headers = line.split(',')
 
      # Get the number of attributes (cols)
      NumofAttributes = len(headers)

      for x in range(NumofAttributes):
        # Check if col should be ignored (starts with '?')
        if headers[x][0] == '?':
          IgnoreList.append(x)
        else:
          row.append(headers[x])
      
      Data.append(row)
      row1 = False
      Line_Num += 1

if __name__ == "__main__":
  main()

