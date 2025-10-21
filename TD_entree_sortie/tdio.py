import matplotlib.pyplot as plt

def listefile(filename):
    res=[]
    with open(filename,'r') as f:
        for line in f:
            line=line.strip()
            Linfo=line.split()
            res.append((Linfo[0],Linfo[5],Linfo[8:]))
    return res


def distribution(filename):
    res=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open(filename,'r') as f:
        for line in f:
            line=line.strip()
            Linfo=line.split()
            time_beg=int(Linfo[5])
            time_end=(len(Linfo[8:])*5+time_beg)//3600
            time_beg=time_beg//3600
            for i in range(time_beg,(time_end+1)):
                res[i]+=1
    return res

#l=distribution("flights.txt")

def histogram(distri):
    plt.bar([i for i in range(24)], distri)
    plt.show()

#histogram(l)

def output(distri,filename):
    with open(filename,'w') as f:
        f.write("-----------------------\n")
        f.write("|   time   | flights  |\n")
        f.write("-----------------------\n")
        for i in range(24):
            f.write(f'| {i:02d}:00:00 |{distri[i]: >10}|\n')
#output(l,'test.txt')


def distributionda(filename):
    resd=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    resa=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open(filename,'r') as f:
        for line in f:
            line=line.strip()
            Linfo=line.split()
            time_beg=int(Linfo[5])
            time_end=(len(Linfo[8:])*5+time_beg)//3600
            time_beg=time_beg//3600
            if Linfo[0]=="DEP":
                for i in range(time_beg,(time_end+1)):
                    resd[i]+=1                  
            else:
                for i in range(time_beg,(time_end+1)):
                    resa[i]+=1
    return list(zip(resd,resa))

#distributionda("flights.txt")
def distributionda(filename,graine=3600):
    resd=[0 for i in range(86400//graine+1)]
    resa=[0 for i in range(86400//graine+1)]
    with open(filename,'r') as f:
        for line in f:
            line=line.strip()
            Linfo=line.split()
            time_beg=int(Linfo[5])
            time_end=(len(Linfo[8:])*5+time_beg)//graine
            time_beg=time_beg//graine
            if Linfo[0]=="DEP":
                for i in range(time_beg,(time_end+1)):
                    resd[i]+=1                  
            else:
                for i in range(time_beg,(time_end+1)):
                    resa[i]+=1
    return list(zip(resd,resa))
l=distributionda("flights.txt",1000)
def output(distri,filename,graine=3600):
    time="time"
    dep="dep"
    arr="arr"
    total="total"
    with open(filename,'w') as f:
        f.write('-'*36)
        f.write('\n')
        f.write(f'|{time: ^10}|{dep: ^7}|{arr: ^7}|{total: ^7}|\n')
        f.write('-'*36)
        f.write('\n')
        for i in range(86400//graine):
            s=i*graine
            afficheh=f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"
            f.write(f'|{afficheh: ^10}|{distri[i][0]: >7}|{distri[i][1]: >7}|{distri[i][0]+distri[i][1]: >7}|\n')

output(l,"q8.txt",1000)
