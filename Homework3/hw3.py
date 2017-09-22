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