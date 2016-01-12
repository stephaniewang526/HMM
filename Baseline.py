#!/usr/bin/env python

train = open('train.txt')
test = open('test.txt')

def containsAssoc(lst, ele):
    for i in range(0,len(lst)):
        tup = lst[i]
        print(type(tup))
        print(tup[0])
        print(tup[1])
        if ele == tup[0]:
            return i
    return -1
    
def preprocess(train):
    lexicon = dict()
    x = 1
    while(True):
        line = train.readline()
        if not line:
            break
        if (x%3==1):
            word_lst = line.split()
        if (x%3==0):
            ner_lst = line.split()
            for i in range(0,len(word_lst)):
                if(ner_lst[i] != 'O'):
                    if word_lst[i] not in lexicon:
                        lexicon[word_lst[i]] = {ner_lst[i] : 1}
                    else: #word has been found before
                        if ner_lst[i] not in lexicon[word_lst[i]]:
                           lexicon[word_lst[i]][ner_lst[i]] = 1
                        else:
                            lexicon[word_lst[i]][ner_lst[i]] = lexicon[word_lst[i]][ner_lst[i]] + 1
        x=x+1
                    
    return lexicon


def createBaseline(lexicon):
    for key in lexicon:
        max_no = 0
        for ner in lexicon[key]:
            if lexicon[key][ner] > max_no:
                max_no = lexicon[key][ner]
                max_ner = ner
        lexicon[key] = max_ner 
    return lexicon

def runTest(test, lexicon):
    x = 1
    per = "PER,"
    loc = "LOC,"
    org = "ORG,"
    misc = "MISC,"
    while(True):
        line = test.readline()
        if not line:
            break
        if (x%3==1):
            word_lst = line.split()
        if (x%3==0):
            pos_lst = line.split()
            for i in range(0,len(word_lst)):
                word = word_lst[i]
                pos = pos_lst[i]
                if word in lexicon:
                    if "PER" in lexicon[word]:
                        per += (pos + "-" + pos + " ")
                    if "LOC" in lexicon[word]:
                        loc += (pos + "-" + pos + " ")
                    if "ORG" in lexicon[word]:
                        org += (pos + "-" + pos + " ")
                    if "MISC" in lexicon[word]:
                        misc += (pos + "-" + pos + " ")
        x+=1
    output = open('output.txt', 'w')
    output.write(per + "\n" + loc + "\n" + org + "\n" + misc)
    output.close()
    
baseline = createBaseline(preprocess(train))

runTest(test, baseline)