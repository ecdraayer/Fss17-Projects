import random
import numpy as np
import math
import sys
class SuperRange:
  def __init__(self):
  	self.label = 0
  	self.most = 0.0
  	self.data = []

  def __str__(self):
    result = "{label= %d, most= %f}" % (self.label, self.most)
    return result

class Range:
  def __init__(self):
  	self.hi = (-2)**63
  	self.lo = 2**63
  	self.n = 0
  	self.span = 0.0
  	self.values = []

  def __str__(self):
  	result = "{span = %f, lo= %f, n= %d, hi= %f}" % (self.span,self.lo,self.n,self.hi)
  	return result

def update(R, v):
  	
  v = x(v)
  if R.lo > v:
    R.lo = v
  if R.hi < v:
  	R.hi = v

  R.values.append(v)
  R.n += 1
  R.span = R.hi - R.lo
  return R

 

def CreateUnsupervisedRange(data):
  
  # Sort Data
  data = np.sort(data, axis=0)
  # Calculate bin size
  s = len(data)
  bin_size = math.sqrt(s)
 
  # Calculate range difference(epislon)
  std = np.std(data, axis=0)
  eps = 0.2*std[0]

  ranges = []

  Bin = []
  r_indx = 0
  ranges = Range()
  last = 0.0
  m = np.max(data)
 
  for i, d in enumerate(data):
    ranges = update(ranges, d)
    if ((ranges.n > bin_size) and 
       (ranges.span > eps) and 
       ((s - i) > bin_size) and
       ((m - x(d)) > eps)):
      Bin.append(ranges)
      ranges = Range()
  
  if ranges.n != 0:
    Bin.append(ranges)
  return Bin


def CreateSuppervisedRange(data, ranges, labels): 
  s_ranges = [None]*len(labels)
  for l in range(len(labels)):
  	s_ranges[l] = SuperRange()
  	s_ranges[l].label = l

  data = np.sort(data, axis=0)
  data = data[:,0]
  
  for index in range(len(data)):
  	if data[index]<labels[0]:
  	  s_ranges[0].data.append(data[index])
  	  if s_ranges[0].most < data[index]:
  	  	s_ranges[0].most = data[index]

  	elif data[index]<labels[1]:
  	  s_ranges[1].data.append(data[index])
  	  if s_ranges[1].most < data[index]:
  	    s_ranges[1].most = data[index]
  	elif data[index]<labels[2]:
  	  s_ranges[2].data.append(data[index])
  	  if s_ranges[2].most < data[index]:
  	    s_ranges[2].most = data[index]
  	elif data[index]<labels[3]:
  	  s_ranges[3].data.append(data[index])
  	  if s_ranges[3].most < data[index]:
  	    s_ranges[3].most = data[index]
  
  return s_ranges

def y(z):
  return z[1]
def x(z):
  return z[0]

def main():
  data = list(np.random.random((50)))

  
  for i, x in enumerate(data):
  	y = 2*np.random.rand()/100
  	if x < 0.2:
  	  y += 0.2
  	elif x < 0.6:
  	  y += 0.6
  	else:
  	  y += 0.9
  	data[i] = [x, y]


  print "We have many unsupervised ranges."
  Unsup_ranges = CreateUnsupervisedRange(data)
  
  i = 1
  for r in Unsup_ranges:
  	print "%d: " %i,
  	i += 1
  	print r

  print 
  print "We have fewer supervised ranges."
  Super_ranges = CreateSuppervisedRange(data, Unsup_ranges, [0.2,0.6,0.9,1])
  for s in Super_ranges:
  	print "super",
  	print s

if __name__ == "__main__":
  main()