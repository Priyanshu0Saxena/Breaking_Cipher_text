import random
import os
import time
#-------Loading Data Phase-----------
def getEncryptedText():
    f=input()
    text = f.split()
    realcipher=[]
    for word in text:
        word = word.replace(",","").replace("!","").replace(";","").replace(".","")
        realcipher.append(word)
    return text,realcipher

plainEncrypted,encrypted_text = getEncryptedText()


def getFrequencyCount(text):
    frequency = {}
    for word in text:
        for letter in word:
            if letter in frequency:
                frequency[letter] += 1
            else:
                frequency[letter] = 1
    return frequency

frequency = dict(sorted(getFrequencyCount(encrypted_text).items(), key = lambda x: x[1], reverse = True))


def generateInitialKey(frequency):
    keyCharacters=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "#", "$", "z", "y", "x", "w", "v", "u", "t", "s", "r", "q", "p", "o", "n"]
    usedSymbol = []
    key=[]
    for i,j in frequency.items():
        usedSymbol.append(i)
        key.append(i)
    for i in keyCharacters:
        if i not in key:
            key.append(i)
            usedSymbol.append(i)
    freq_order = [4,19,0,14,8,13,17,18,7,3,11,20,2,12,5,24,22,6,15,1,21,10,23,16,9,25]
    ind=int(0)
    for i in freq_order:
        key[i]=usedSymbol[ind]
        ind=ind+1
    return key


def generateRandomKey():
    keyCharacters=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "#", "$", "z", "y", "x", "w", "v", "u", "t", "s", "r", "q", "p", "o", "n"]
    random.shuffle(keyCharacters)
    return keyCharacters

initialKey=generateInitialKey(frequency)

def decrypt(encryption, key):
    decryption = []
    for word in encryption:
        newWord=""
        for letter in word:
            if letter in key:
                newWord = newWord + chr(key.index(letter)+97)
            else:
                newWord = newWord + letter
        decryption.append(newWord)
    return decryption

def validWordS():
    setOfWords=set()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, "bigDictionary.txt")
    with open(full_path,"r") as f:
        text = f.read().split()
        for word in text:
            setOfWords.add(word)
    return setOfWords

validword=validWordS()

def getDesiredKey(key):
    for i in range(26):
        if key[i] not in frequency:
            key[i]="x"


#------- Actual Algorithm starts-----

def weight(decryption):
    score=0
    mostCommonWords = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their",
    "is", "are", "was", "were", "been", "being"
    ]
    commonWords = [
    "if", "about", "who", "which", "when", "what", "so", "up", "out", "into",
    "than", "then", "them", "these", "those", "because", "while", "where",
    "how", "why", "after", "before", "over", "under", "again", "still",
    "such", "many", "much", "more", "most", "some", "any", "each", "every",
    "other", "same", "new", "old", "long", "great", "little", "own",
    "right", "left", "high", "small", "large", "early", "late"
    ]
    valid3gram=["the","and","ing","her","ere","ent","tha","nth","was","eth","for","dth","has","hes","his","oft","sth","men","ion","all","tio","ver","ter","est","ers","ati","hat","ate","res"]
    valid2gram = ["th","he","in","er","an","re","on","at","en","nd","ti","es","or","te","of","ed","is","it","al","ar","st","to","nt","ng","se","ha","as","ou","io","le","ve"]
    for word in decryption:
        if word in mostCommonWords:
            score+=4
        elif word in commonWords:
            score+=3
        elif word in validword:
            score+=1
        else:
            i=0
            j=3
            while j<len(word):
                if word[i:j] in valid2gram:
                    score+=0.5
                elif word[i:j-1] in valid2gram:
                    score+=0.25
                i=i+1
                j=j+1
    return score

def generateAllNeighbours(key):
    neighbours = []
    n = len(key)

    for i in range(n):
        for j in range(i + 1, n):
            new_key = key.copy()
            new_key[i], new_key[j] = new_key[j], new_key[i]
            neighbours.append(new_key)

    return neighbours

def hillClimb(key, encryption):
    bestOverallKey = key
    decrypted = decrypt(encryption, key)
    bestOverallScore = weight(decrypted)

    restarts = 70
    endtime=time.time()+115
    firstrun=1
    while True:
        if firstrun == 1:
            currentKey=key 
            firstrun=0
        else:
            currentKey=generateRandomKey()
        decrypted = decrypt(encryption, currentKey)
        currentScore = weight(decrypted)
        
        while True:
            bestKey = currentKey
            bestScore = currentScore

            for k in generateAllNeighbours(currentKey):
                d = decrypt(encryption, k)
                s = weight(d)

                if s > bestScore:
                    bestScore = s
                    bestKey = k

            if bestScore <= currentScore:
                break

            currentKey = bestKey
            currentScore = bestScore

        if currentScore > bestOverallScore:
            bestOverallScore = currentScore
            bestOverallKey = currentKey


        if time.time() >=endtime:
            break

    return bestOverallKey

finalKey=hillClimb(initialKey,encrypted_text)
print("Deciphered Plaintext:"," ".join(decrypt(plainEncrypted,finalKey)))
getDesiredKey(finalKey)
print("Deciphered Key:","".join(finalKey))