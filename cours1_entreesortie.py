def filter_words(words_file,filter):
    res=[]
    with open(words_file,'r') as f:
        for line in f:
            line=line.rstrip()
            if filter(line):
                res.append(line)
    return res

def filter_words2(words_file,filter):
    with open(words_file,'r') as f:
        res=[ line.rstrip() for line in f if filter(line.rstrip())]
    return res

def edit_words(words,output_file):
    with open(output_file,'w') as f:
        for m in words:
            f.write(m)
            f.write('\n')


def fltr(m,c='z'):
    return m[0]==c


def main():
    w=filter_words2("/usr/share/dict/words",fltr)
    edit_words(w,"resexo1v2.txt")
    return 0

main()
