def fun(s1):
    d={}
    c=0
    for i in s1:
        d[i]=d.get(i,0)+1
    for i in d:
        if d[i]<=1:
            c+=1
    print(c)
    return c


def che(s,words):
    d={}
    # for i in s:
        # d[i]=1
    c=0
    for i in words:
        if i in s:
            print(i)
            c+=len(i)
            if c==len(s):
                return True



    return False




v=che("AllTheBest",["best","of","Luck","All","Best","The"])
print(v)