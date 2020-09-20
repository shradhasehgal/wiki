import sys
import math
import os
from nltk.stem.snowball import SnowballStemmer
# from nltk.corpus import stopwords 
import re
from datetime import datetime
import linecache

# stop_words = set(stopwords.words('english')) 
stems = {}
stemmer = SnowballStemmer("english")
stop_words = set(['whence', 'here', 'show', 'were', 'why', 'nt', 'the', 'whereupon', 'not', 'more', 'how', 'eight', 'indeed', 'i', 'only', 'via', 'nine', 're', 'themselves', 'almost', 'to', 'already', 'front', 'least', 'becomes', 'thereby', 'doing', 'her', 'together', 'be', 'often', 'then', 'quite', 'less', 'many', 'they', 'ourselves', 'take', 'its', 'yours', 'each', 'would', 'may', 'namely', 'do', 'whose', 'whether', 'side', 'both', 'what', 'between', 'toward', 'our', 'whereby', "'m", 'formerly', 'myself', 'had', 'really', 'call', 'keep', "'re", 'hereupon', 'can', 'their', 'eleven', '’m', 'even', 'around', 'twenty', 'mostly', 'did', 'at', 'an', 'seems', 'serious', 'against', "n't", 'except', 'has', 'five', 'he', 'last', '‘ve', 'because', 'we', 'himself', 'yet', 'something', 'somehow', '‘m', 'towards', 'his', 'six', 'anywhere', 'us', '‘d', 'thru', 'thus', 'which', 'everything', 'become', 'herein', 'one', 'in', 'although', 'sometime', 'give', 'cannot', 'besides', 'across', 'noone', 'ever', 'that', 'over', 'among', 'during', 'however', 'when', 'sometimes', 'still', 'seemed', 'get', "'ve", 'him', 'with', 'part', 'beyond', 'everyone', 'same', 'this', 'latterly', 'no', 'regarding', 'elsewhere', 'others', 'moreover', 'else', 'back', 'alone', 'somewhere', 'are', 'will', 'beforehand', 'ten', 'very', 'most', 'three', 'former', '’re', 'otherwise', 'several', 'also', 'whatever', 'am', 'becoming', 'beside', '’s', 'nothing', 'some', 'since', 'thence', 'anyway', 'out', 'up', 'well', 'it', 'various', 'four', 'top', '‘s', 'than', 'under', 'might', 'could', 'by', 'too', 'and', 'whom', '‘ll', 'say', 'therefore', "'s", 'other', 'throughout', 'became', 'your', 'put', 'per', "'ll", 'fifteen', 'must', 'before', 'whenever', 'anyone', 'without', 'does', 'was', 'where', 'thereafter', "'d", 'another', 'yourselves', 'n‘t', 'see', 'go', 'wherever', 'just', 'seeming', 'hence', 'full', 'whereafter', 'bottom', 'whole', 'own', 'empty', 'due', 'behind', 'while', 'onto', 'wherein', 'off', 'again', 'a', 'two', 'above', 'therein', 'sixty', 'those', 'whereas', 'using', 'latter', 'used', 'my', 'herself', 'hers', 'or', 'neither', 'forty', 'thereupon', 'now', 'after', 'yourself', 'whither', 'rather', 'once', 'from', 'until', 'anything', 'few', 'into', 'such', 'being', 'make', 'mine', 'please', 'along', 'hundred', 'should', 'below', 'third', 'unless', 'upon', 'perhaps', 'ours', 'but', 'never', 'whoever', 'fifty', 'any', 'all', 'nobody', 'there', 'have', 'anyhow', 'of', 'seem', 'down', 'is', 'every', '’ll', 'much', 'none', 'further', 'me', 'who', 'nevertheless', 'about', 'everywhere', 'name', 'enough', '’d', 'next', 'meanwhile', 'though', 'through', 'on', 'first', 'been', 'hereby', 'if', 'move', 'so', 'either', 'amongst', 'for', 'twelve', 'nor', 'she', 'always', 'these', 'as', '’ve', 'amount', '‘re', 'someone', 'afterwards', 'you', 'nowhere', 'itself', 'done', 'hereafter', 'within', 'made', 'ca', 'them'])
query_file = sys.argv[1]
total_docs = 9829059

keyToPos = {'t':0, 'i':1, 'c':2, 'l':3, 'r':4, 'b':5}

finalFolder = "final_index"
firstWords = []
mergeWords = open(os.path.join(finalFolder, "mergeWords.txt"),"r")
lines = mergeWords.readlines()
for line in lines:
    firstWords.append(line.strip())


# docTitles = []
# docTitlesFile = open("titles.txt","r")
# lines = docTitlesFile.readlines()
# for line in lines:
#     docTitles.append(line.strip())
queries = open(query_file, 'r')
results = open("queries_op.txt", "w")

def floorSearch(low, high, x):  
  
    if (low > high):  
        return -1
  
    if (x >= firstWords[high]):  
        return high  
  
    mid = int((low + high) / 2)  
  
    if (firstWords[mid] == x):  
        return mid  
  
    if (mid > 0 and firstWords[mid-1] <= x  and x < firstWords[mid]):  
        return mid - 1
   
    if (x < firstWords[mid]):  
        return floorSearch(low, mid-1, x)  
  
    return floorSearch(mid + 1, high, x)  

def custom(doc):
    key = 'd'
    arr = {'t':0, 'i':0, 'c':0, 'l':0, 'r':0, 'b':0}
    docID = 0
    # print(doc)
    cur = ""
    for i in range(len(doc)):
        if doc[i].isalpha():
            if key == 'd':
                docID = cur
            else:        
                arr[key] = int(cur)
                    
            key = doc[i]
            cur = ""
        else:
            cur += doc[i]
    
    return docID, arr

while True:
    query = queries.readline()
    if not query:
        break
    else:
        begin = datetime.now()
        parts = query.lower().split(",")
        k = int(parts[0])
        searchStr = parts[1].strip()
        # print(searchStr)


        words = {}
        if ":" in searchStr:
            temps = searchStr.split(':')
            for i in range(1, len(temps)):
                if i == len(temps) -1:
                    words[temps[i-1][-1]] = temps[i]
                else:
                    words[temps[i-1][-1]] = temps[i][: -2]

        else:
            words['a'] = searchStr
    

        doc_scores = {}
        for key, val in words.items():
            val = re.split(r'[^a-z0-9]+', val)
            searchTerms = []
            for w in val: 
                if w not in stop_words:
                    stemmed_w = stemmer.stem(w)
                    searchTerms.append(stemmed_w)


            for term in searchTerms:
                x = floorSearch(0, len(firstWords)-1, term) 
                found = 0
                f = open(os.path.join(finalFolder, str(x)+".txt"), "r")

                while True:
                    line = f.readline()
                    # print(word)
                    posting = line.split(':')
                    if found or len(posting) !=2:
                        break
                    word = posting[0]
                    # print(word)
                    if word == term:
                        found = 1

                        postingList = posting[1]
                        docs = postingList.split("d")

                        field_count = 0

                        if key == "a":
                            for doc in docs:
                                docID, arr = custom(doc)
                                tfidf = math.log(1+20*arr['t'] + 1*arr['b'] + 5*arr['c'] + 0.3*arr['l'] + 0.1*arr['r'] + 10*arr['i'], 10)*math.log(total_docs/len(docs), 10)
                                if docID not in doc_scores:
                                    doc_scores[docID] = tfidf
                                else:
                                    doc_scores[docID] += tfidf          
                        else:
                            for doc in docs:
                                docID, arr = custom(doc)
                                tfidf = math.log(1+20*arr['t'] + 1*arr['b'] + 5*arr['c'] + 0.3*arr['l'] + 0.1*arr['r'] + 10*arr['i']+ 1000*arr[key], 10)*math.log(total_docs/len(docs), 10)
                                if docID not in doc_scores:
                                    doc_scores[docID] = tfidf
                                else:
                                    doc_scores[docID] += tfidf                     
        
        # print("time to parse is ", parse_end-begin)

        sorted_docs = sorted(doc_scores.items(), key=lambda x: -x[1])
        cur = 0
        for i in sorted_docs:
            if cur == k:
                break
            
            docc = int(i[0]) +1
            read = int(docc / 2000)
            number  = docc %2000
            # print(linecache.getline("titles.txt", docc))
            docname = linecache.getline("final_index/titles/"+str(read)+".txt", number)
            # print(docname)
            results.write(i[0] + ", "+ docname)
            # results.write(docTitles[int(i[0])-1]+"\n0")
            cur += 1

        if(len(sorted_docs) < k):
            req = k - len(sorted_docs)
            i = 1
            while req:
                if i not in doc_scores:
                    read = int(i/2000)
                    number = i%2000
                    docname = linecache.getline("final_index/titles/"+str(read)+".txt", number)
                    # print(docname)
                    results.write(str(i) + ", "+ docname)
                    req -= 1
                i += 1
        
        parse_end = datetime.now()
        time_taken = parse_end - begin
        # print(time_taken)
        results.write(str(time_taken) +", "+ str(time_taken/k)+"\n\n")


