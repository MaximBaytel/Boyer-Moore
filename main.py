__author__ = 'm.baytel'

import sys

def ZPreprocessing(pattern):
    if pattern is None or len(pattern) == 0:
        raise ValueError('Bad pattern')

    right=left=0
    Zarray=[0]*len(pattern)

    Zindex=1 #for zero it is meaningless

    while Zindex < len(pattern):
        #if it is out previous prefix we know nothing
        if Zindex > right:
            length=0
            i=0
            j=Zindex
            #straightforward comparison
            while j<len(pattern) and pattern[i] == pattern[j] :
                i+=1
                j+=1
                length+=1
            Zarray[Zindex]=length

            if length:
                left=Zindex
                right=j-1

        else:
            
            #for symbols 0...right-left already calculated            
            if Zarray[Zindex-left] < right-Zindex or Zarray[Zindex-left]==0:
                Zarray[Zindex]=Zarray[Zindex-left]
            else:
                #all these symbols are needed straightforward comparisons
                i=right-left+1
                j=right+1
                #length=Zarray[Zindex-left]
                length=(right-Zindex)+1

                while j<len(pattern) and pattern[i] == pattern[j]:
                    i+=1
                    j+=1
                    length+=1

                Zarray[Zindex]=length

                if length > right-Zindex:
                    left=Zindex
                    right=j-1

        Zindex += 1

    return Zarray


#print(ZPreprocessing('aabcaabxaaz'))

def goodSuffixPreprocessing(pattern):
    if pattern is None or len(pattern) == 0:
        raise ValueError('Bad pattern')

    reversePattern=pattern[::-1]

    #print(reversePattern)

    Zarray=ZPreprocessing(reversePattern)

    #print('Zarray',Zarray)

    lenPattern=len(pattern)

    goodsuffAray=[-1]*lenPattern #-1 is a marker

    for j in reversed(range(1,lenPattern)):

        index=Zarray[j]
        if index <= 0:
            continue

        goodsuffAray[lenPattern-index]=lenPattern-j-index

    #preprocessing for third rule and Galil rule is here because it is needed Zarray    

    last=lenPattern


    maxSuffArray = [0]*lenPattern

    for k in reversed(range(0,lenPattern)):
        if Zarray[k]+k == lenPattern:
            last=k
        maxSuffArray[k]=last


    return goodsuffAray,maxSuffArray

def badCharPreprocessing(pattern):
     if pattern is None or len(pattern) == 0:
        raise ValueError('Bad pattern')

     badArray=[-1]*128 
     j=0

     for character in pattern:
         badArray[ord(character)]=j
         j+=1

     return badArray


def BoyerMoore(T,pattern):
    if pattern is None or len(pattern) == 0 or T is None or len(T) == 0:
        raise ValueError('Bad arguments')

    goodsuffArray,maxSuffArray = goodSuffixPreprocessing(pattern)
    badCharArray  = badCharPreprocessing(pattern)

    #print('maxSuffArray',maxSuffArray)

    i=0

    lenPattern = len(pattern)
    lenT       = len(T)
    lowIndex=0 #for Galil rule 

    res = []

    while i+lenPattern <= lenT:
        #print('Curr index=',i)
        #print('Low index=',lowIndex)
        j = lenPattern - 1 #always at the end of pattern when comparison is started

        if pattern[j] != T[i+j]: 
            i+=1
            lowIndex=0
            #print('Last character mismatch')
            continue

        j-=1 #if symbols are matched it will be shifted

		#while symbols are matched it will be shifted but left bound for shift is lowIndex. lowIndex is 0 or is set according to Galil rule        
        while j>= lowIndex and pattern[j] == T[i+j]:
            j-=1

        #has match?
        if j < lowIndex:
            res.append(i+1) 
            i+=maxSuffArray[0] #Third rule
            lowIndex = lenPattern - maxSuffArray[0] # for Galil rule 
            continue

        if j<0: #for debug...
            raise ValueError('j<0!!!')


        if goodsuffArray[j+1]>j: #for debug...
            raise ValueError('Suffix to the right than j!!! j=' + str(j))


        shift = max(j-goodsuffArray[j+1]+1,j-badCharArray[ord(T[i+j])])
        #index = min(badCharArray[ord(T[i+j])],goodsuffArray[j+1])

        if shift>j: 
            i+=maxSuffArray[j+1]
            lowIndex = lenPattern - (maxSuffArray[j+1])
            continue

        #if flow is here then letter rule or suffix rule may be applied        

        i+= shift
        lowIndex=0 #not actual

    return res


#print(BoyerMoore('cabdabdab','bd'))
#print(BoyerMoore('cabdabdab','xyz'))

#print(BoyerMoore('aaGHGHIJIHHIGHGHIJIH','ADAEDACBBB'))

#quit()

if len(sys.argv) != 3:
    print('Usage ' + sys.argv[0] + ' <string> <pattern>')
    quit()

res = BoyerMoore(sys.argv[1],sys.argv[2])

print(*res, sep=' ')
