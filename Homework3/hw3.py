import sys
def unsuperRanges():
  pass

def superRanges():
  pass

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata


def local_distance(template_frame, test_frame):
  assert type(template_frame) == type(test_frame) == list
  
  D = 0
  for i in range(len(template_frame)):
    D += abs(template_frame[i] - test_frame[i])

  return D

def main():
  
  for i in range(len(template)):
    for j in range(len(test)):

      # Edge Case
      if (i==0) and (j==0):
         global_distance[i][j] = local_distance(template[i], test[j])
         backpointer[i][j] = (None,None)
      
      elif (i==0):
        assert global_distance[i][j-1] >= 0
        global_distance[i][j] = global_distance[i][j-1] + local_distance(template[i], test[j])
        backpointer[i][j] = (i,j-1)
 
      elif (j==0):
         assert global_distance[i-1][j] >= 0 
         global_distance[i][j] = global_distance[i-1][j] + local_distance(template[i], test[j])
         backpointer[i][j] = (i-1,j)
 
      else:
         assert global_distance[i][j-1]   >= 0
         assert global_distance[i-1][j]   >= 0
         assert global_distance[i-1][j-1] >= 0
 
         lowest_global_distance = w_h * global_distance[i-1][j]
         backpointer[i][j] = (i-1,j)
 
         if (w_v * global_distance[i][j-1]) < lowest_global_distance:
           lowest_global_distance = w_v * global_distance[i][j-1]
           backpointer[i][j] = (i,j-1)
     
         if (w_d * global_distance[i-1][j-1]) < lowest_global_distance:
           lowest_global_distance = w_d * global_distance[i-1][j-1]
           backpointer[i][j] = (i-1,j-1)

         global_distance[i][j] = lowest_global_distance + local_distance(template[i], test[j])

  D = global_distance[len(template)-1][len(test)-1]

  alignment = []
  i,j = len(template)-1, len(test)-1
  alignment.append( (i,j) )

  # Generate Random Numbers

  #for i, value in enumerate(randoms):
  '''
  if z < 0.2 then return 0.2 + 2*R.r()/100 end
  if z < 0.6 then return 0.6 + 2*R.r()/100 end
  return 0.9 + 2*R.r()/100 end
  '''
  f = open('output', 'w')
  f.write("UnSupervised Ranges:\n")
  f.write("Supervised Ranges:\n")
  f.close()

if __name__ == "__main__":
  main()