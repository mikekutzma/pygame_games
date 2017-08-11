import matplotlib.pyplot as plt
import sys
import codecs

filename = sys.argv[1]

with codecs.open(filename) as f:
	x = [int(a.rstrip("\n")) for a in f.readlines()]

plt.plot(x)
plt.show()