from collections import Counter


a = [1, 1, 1]
b = [1, 2, 2]
c = [2, 2, 3]

d = zip(a, b, c)

for i in d:
	print(Counter(i).most_common(1)[0][0])