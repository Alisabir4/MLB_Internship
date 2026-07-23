sentence="python is an easy language"
words=sentence.split()
frequency={}
for word in words:
    if word in frequency:
        frequency[word]+=1
    else:
        frequency[word]=1
print("frequency of word in the sentence is : ",frequency)
        