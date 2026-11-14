import sys,struct
d=open(sys.argv[1],'rb').read(); i=0;k=0
while i<len(d):
    n=struct.unpack('>Q',d[i:i+8])[0]; i+=8
    open(f'{sys.argv[2]}{k}.png','wb').write(d[i:i+n]); i+=n; k+=1
print(k)
