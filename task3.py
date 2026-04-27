s = input ("enter string : ")
words = s.split()
w = {}

for i in words:
    w[i] = w.get(i, 0) + 1  ## error 

for i, count in w.items():
    print(f"{i} : {count}")
