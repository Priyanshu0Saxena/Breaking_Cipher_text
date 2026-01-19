import random
import os

#-------Loading Data Phase-----------
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

plainEncrypted,encrypted_text = getEncryptedText("samplecipher.txt")


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
# initialKey = generateRandomKey()

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

def fourGramWords():
    setof4gram={}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, "4gram.txt")
    with open(full_path,"r") as f:
        text=f.read().split()
        i=0
        while i+1 < len(text):
            setof4gram[text[i]]=int(text[i+1])
            i=i+2
    return setof4gram

valid4Gram=fourGramWords()

#------- Actual Algorithm starts-----
def ngramScore(decryption):
    score=0
    for word in decryption:
        if len(word) >= 4:
            i=0
            j=3
            while j <= len(word):
                if word[i:j+1] in valid4Gram:
                    score += valid4Gram[word[i:j+1]]
                else:
                    score -= 5
                i=i+1
                j=j+1
    return score



def validWordScore(decryption):
    score=0
    for word in decryption:
        if word in validword:
            score+=1
    return score

def weightOfMostCommonWords(decrypted):
    score=0
    mostCommonWords = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their",
    "is", "are", "was", "were", "been", "being"
    ]
    for word in decrypted:
        if word in mostCommonWords:
            score = score+1
    return score

def weightOfCommonWords(decrypted):
    score=0
    commonWords = [
    "if", "about", "who", "which", "when", "what", "so", "up", "out", "into",
    "than", "then", "them", "these", "those", "because", "while", "where",
    "how", "why", "after", "before", "over", "under", "again", "still",
    "such", "many", "much", "more", "most", "some", "any", "each", "every",
    "other", "same", "new", "old", "long", "great", "little", "own",
    "right", "left", "high", "small", "large", "early", "late"
    ]
    for word in decrypted:
        if word in commonWords:
            score = score + 1
    return score

def weight(decryption):
    return 3*weightOfMostCommonWords(decryption) + 2* weightOfCommonWords(decryption) + validWordScore(decryption)

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
    bestOverallScore = weight(decrypt(encryption, key))
    restarts = 10
    for _ in range(restarts):
        currentKey = generateRandomKey()
        currentScore = weight(decrypt(encryption, currentKey))

        while True:
            bestKey = currentKey
            bestScore = currentScore

            for k in generateAllNeighbours(currentKey):
                s = weight(decrypt(encryption, k))
                if s > bestScore:
                    bestScore = s
                    bestKey = k

            if bestScore <= currentScore:
                print(bestScore)
                break  

            currentKey = bestKey
            currentScore = bestScore

        if currentScore > bestOverallScore:
            bestOverallScore = currentScore
            bestOverallKey = currentKey

    return bestOverallKey


finalKey=hillClimb(initialKey,encrypted_text)
print("key selected is: ",finalKey)
print("decrypted text: ",decrypt(encrypted_text,finalKey))