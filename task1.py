s = input("Enter String : ")
a = []
a.append(s)
v = len(s.replace(" " , ""))
print(len(s))
print(v)

copy_s = a.copy()
copy_s = a.reverse()


if (copy_s == a):
    print("palindrome")
else:
    print("not palindrome")


m = ['a','e','i','o','u']
##s = input("Enter String : ")
vovel_count = 0
consonent_count = 0
for i in s :
    if i  in m :
      vovel_count += 1
    else:
      consonent_count+=1
print (vovel_count)
print(consonent_count)


"""m = ['a','e','i','o','u']
##s = input("Enter String : ")
for i in s :
    if i not in m :
        count += 1
print (count)
        
        """





