def getEncryptedText(textFile):
    with open(textFile,"r") as f:
        text = f.read().split()
        realcipher=[]
        for word in text:
            word = word.replace(",","").replace("!","").replace(";","").replace(".","")
            realcipher.append(word)
        return realcipher
        
def getFrequencyCount(text):
    frequency = {}
    for word in text:
        for letter in word:
            if letter in frequency:
                frequency[letter] += 1
            else:
                frequency[letter] = 1
    return frequency

encrypted_text = getEncryptedText("samplecipher.txt")
print(encrypted_text)
frequency = dict(sorted(getFrequencyCount(encrypted_text).items(), key = lambda x: x[1], reverse = True))
for key,value in frequency.items():
    print(key," ",value)