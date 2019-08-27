

def gcd(a, m, n):
	if m % n:
		a.append(n)
		return gcd(a, n, m%n)

	else:
		return a
		#rtype: List[int]

t = []
b = []
c = []
t = gcd(b ,65668,436)
print(b," -> b")
print(t," -> gcd的return為List")

gcd(c, 12, 10)
b.extend(c)
print(c," -> c")
print(b," -> b+c")