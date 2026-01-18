import random
import os
def getEncryptedText(textFile):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, textFile)
    with open(full_path,"r") as f:
        text = f.read().split()
        realcipher=[]
        for word in text:
            word = word.replace(",","").replace("!","").replace(";","").replace(".","")
            realcipher.append(word)
        return text,realcipher

def getFrequencyCount(text):
    frequency = {}
    for word in text:
        for letter in word:
            if letter in frequency:
                frequency[letter] += 1
            else:
                frequency[letter] = 1
    return frequency

def generateInitialKey(frequency):
    usedSymbol = []
    key=[]
    for i,j in frequency.items():
        usedSymbol.append(i)
        key.append(i)
    unused="z"
    while unused in usedSymbol:
        unused = chr(ord(unused[0])+1)
    while len(usedSymbol) <= 25:
        usedSymbol.append(unused)
        key.append(unused)
    freq_order = [4,19,0,14,8,13,17,18,7,3,11,20,2,12,5,24,22,6,15,1,21,10,23,16,9,25]
    ind=int(0)
    for i in freq_order:
        key[i]=usedSymbol[ind]
        ind=ind+1
    return key

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

def ngramScore():

def validWordScore():

def weight(decryption):
    return 0.7 * ngramScore(decryption) + 0.3 * validWordScore(decryption)

def hillClimb():

def generateNeighbour():


plainEncrypted,encrypted_text = getEncryptedText("samplecipher.txt")
print(plainEncrypted)
print(encrypted_text)
frequency = dict(sorted(getFrequencyCount(encrypted_text).items(), key = lambda x: x[1], reverse = True))
symbol=[]
for key,value in frequency.items():
    symbol.append(key)
key=generateInitialKey(frequency)