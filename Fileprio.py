import operator

def swap(a,b,l):
    l[a],l[b]=l[b],l[a]


def bubble(l,i,cmp):
    j=(i-1)//2
    while j>= 0 and cmp(l[i],l[j]) :
        swap(i,j,l)
        i=j
        j=(i-1)//2
    
        

def sift_down(l,n,cmp):
    swap(0,n,l)
    n=n-1
    i=0
    while (i<n):
        fg=2*i+1
        fd=fg+1
        j=i
        if (fg<n and not(cmp(l[j],l[fg]))):
            j=fg
        if (fd<n and not(cmp(l[j],l[fd]))):
            j=fd
        if (j==i):
            break
        swap(i,j,l)
        i=j

def heapify(l,cmp):
    n=len(l)
    for i in range(1,n):
        bubble(l,i,cmp)


def heapsort(l,cmp=operator.lt):
    heapify(l,cmp)
    n=len(l)
    print(l)
    for i in reversed(range(n)):
        sift_down(l,i,cmp)
        print(l)
    



#compléxité temporelle O(|l|log(|l|)) pour bubble et sift_down O(log(|l|)
#compléxité heapsort O(|l|log(|l|))
# pas stable
# O(|l|log|l|)
        
    
