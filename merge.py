import os
import heapq
from datetime import datetime

begin = datetime.now()

all_files = []
# N = 10000000000

def getLine(i):
    line = all_files[i].readline().strip("\n")
    if line != "":
        lineParts = line.split(":")
        word = lineParts[0]
        postingList = lineParts[1]
        return Node(word, postingList, i)
    
    return 0


class Node():
    def __init__(self, word, postingList, fileno):
        self.word = word
        self.postingList = postingList
        self.fileno = fileno
        
    def __lt__(self, other):
        if self.word != other.word:
            return self.word < other.word
        else:
            return self.fileno < other.fileno


filecount = 0
for filename in os.listdir("inverted_index"):
    filecount += 1

for i in range(filecount):
    all_files.append(open(os.path.join("inverted_index", str(i) + ".txt")))

heap = [getLine(i) for i in range(len(all_files))]
heapq.heapify(heap)
# heapq.heapify(heap)

finalNumber = 0
words = 0
finalFolder = "final_index"

try:
    os.mkdir(finalFolder)
except FileExistsError:
    print("Dir exists already")

finalIndex = open(os.path.join(finalFolder, str(finalNumber)+".txt"),"w+")
mergeWords = open(os.path.join(finalFolder, "mergeWords.txt"),"w+")
newFile = 1

partial_count = 0
while(len(heap)):
    curWord = heap[0].word
    partial_count += 1
    curPosting = ""  
    if newFile:
        newFile = 0
        mergeWords.write(curWord+"\n")

    while len(heap) and heap[0].word == curWord:
        curPosting += heap[0].postingList
        curFile = heap[0].fileno
        newWord = getLine(curFile)
        heapq.heappop(heap)
        if newWord:
            heapq.heappush(heap, newWord)
    
    # if len(curWord) >1:
    #     sttr = curWord[0] + curWord[1]
    # else:
    #     sttr = curWord
    # finalIndex = open(os.path.join(finalFolder, sttr+".txt"),"a")
    finalIndex.write(curWord+":"+curPosting+"\n")
    # finalIndex.close()
    words += 1
    if not words % 10000:
        finalNumber += 1
        newFile = 1
        finalIndex = open(os.path.join(finalFolder, str(finalNumber)+".txt"),"w+")



stats = open("stats.txt", "a")
stats.write(str(partial_count) + "\n")
stats.close()
parse_end = datetime.now()
print("time to parse is ", parse_end-begin)