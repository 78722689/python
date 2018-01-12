mystr = '91f8b7edab85603c59dc0'
oid = '1.3.6.1.4.1.28458.2.78.5.6.9.1.21.'

for i in mystr:
    oid = oid + str(ord(i)) + '.'
print(oid)