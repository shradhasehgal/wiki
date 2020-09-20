import sys
import xml.sax
from nltk.stem.snowball import SnowballStemmer
import re
from datetime import datetime
import os
import heapq


total_count = 0
THRESHOLD = 100000
overallDict = {}
indexFile = sys.argv[2]
stats = "stats.txt"
fileco = 0

class ParsingHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.text = ""
        self.title = ""
        self.docID = 1
        self.tag = ""
    
    def startElement(self, tag, attributes):
        self.tag = tag

    def endElement(self, tag):
        if tag == "page":
            if not self.docID%THRESHOLD:
                print(fileco)
                createMiniIndex()
                global overallDict 
                overallDict = {}
            index(self.title, self.text, self.docID)
            self.title = ""
            self.text = ""
            self.docID += 1

    def characters(self, content):
        if self.tag == "title":
            self.title += content
        elif self.tag == "text":
            self.text += content

# stop_words = set(stopwords.words('english')) 
stop_words = set(['whence', 'here', 'show', 'were', 'why', 'nt', 'the', 'whereupon', 'not', 'more', 'how', 'eight', 'indeed', 'i', 'only', 'via', 'nine', 're', 'themselves', 'almost', 'to', 'already', 'front', 'least', 'becomes', 'thereby', 'doing', 'her', 'together', 'be', 'often', 'then', 'quite', 'less', 'many', 'they', 'ourselves', 'take', 'its', 'yours', 'each', 'would', 'may', 'namely', 'do', 'whose', 'whether', 'side', 'both', 'what', 'between', 'toward', 'our', 'whereby', "'m", 'formerly', 'myself', 'had', 'really', 'call', 'keep', "'re", 'hereupon', 'can', 'their', 'eleven', '’m', 'even', 'around', 'twenty', 'mostly', 'did', 'at', 'an', 'seems', 'serious', 'against', "n't", 'except', 'has', 'five', 'he', 'last', '‘ve', 'because', 'we', 'himself', 'yet', 'something', 'somehow', '‘m', 'towards', 'his', 'six', 'anywhere', 'us', '‘d', 'thru', 'thus', 'which', 'everything', 'become', 'herein', 'one', 'in', 'although', 'sometime', 'give', 'cannot', 'besides', 'across', 'noone', 'ever', 'that', 'over', 'among', 'during', 'however', 'when', 'sometimes', 'still', 'seemed', 'get', "'ve", 'him', 'with', 'part', 'beyond', 'everyone', 'same', 'this', 'latterly', 'no', 'regarding', 'elsewhere', 'others', 'moreover', 'else', 'back', 'alone', 'somewhere', 'are', 'will', 'beforehand', 'ten', 'very', 'most', 'three', 'former', '’re', 'otherwise', 'several', 'also', 'whatever', 'am', 'becoming', 'beside', '’s', 'nothing', 'some', 'since', 'thence', 'anyway', 'out', 'up', 'well', 'it', 'various', 'four', 'top', '‘s', 'than', 'under', 'might', 'could', 'by', 'too', 'and', 'whom', '‘ll', 'say', 'therefore', "'s", 'other', 'throughout', 'became', 'your', 'put', 'per', "'ll", 'fifteen', 'must', 'before', 'whenever', 'anyone', 'without', 'does', 'was', 'where', 'thereafter', "'d", 'another', 'yourselves', 'n‘t', 'see', 'go', 'wherever', 'just', 'seeming', 'hence', 'full', 'whereafter', 'bottom', 'whole', 'own', 'empty', 'due', 'behind', 'while', 'onto', 'wherein', 'off', 'again', 'a', 'two', 'above', 'therein', 'sixty', 'those', 'whereas', 'using', 'latter', 'used', 'my', 'herself', 'hers', 'or', 'neither', 'forty', 'thereupon', 'now', 'after', 'yourself', 'whither', 'rather', 'once', 'from', 'until', 'anything', 'few', 'into', 'such', 'being', 'make', 'mine', 'please', 'along', 'hundred', 'should', 'below', 'third', 'unless', 'upon', 'perhaps', 'ours', 'but', 'never', 'whoever', 'fifty', 'any', 'all', 'nobody', 'there', 'have', 'anyhow', 'of', 'seem', 'down', 'is', 'every', '’ll', 'much', 'none', 'further', 'me', 'who', 'nevertheless', 'about', 'everywhere', 'name', 'enough', '’d', 'next', 'meanwhile', 'though', 'through', 'on', 'first', 'been', 'hereby', 'if', 'move', 'so', 'either', 'amongst', 'for', 'twelve', 'nor', 'she', 'always', 'these', 'as', '’ve', 'amount', '‘re', 'someone', 'afterwards', 'you', 'nowhere', 'itself', 'done', 'hereafter', 'within', 'made', 'ca', 'them'])
stems = {}
stemmer = SnowballStemmer("english")

def tokenize(text, all):
    words = re.split(r'[^a-z0-9]+', text)
    filtered = []
    global total_count
    if all:
        total_count += len(words)

    for w in words: 
        if w not in stop_words:
            if w not in stems:
                if len(w) > 0 and len(w) < 30:
                    stemmed_w = stemmer.stem(w)
                    filtered.append(stemmed_w)
                    stems[w] = stemmed_w
            else:
                filtered.append(stems[w])

    return filtered

try:
    os.mkdir(indexFile)
except FileExistsError:
    print("Dir exists already")

def createMiniIndex():
    global fileco
    global overallDict
    overallDict = {k:v for k,v in sorted(overallDict.items(), key=lambda item: item[0])}

    wut = ['t', 'i', 'c', 'l', 'r', 'b']
    f = open(os.path.join(indexFile, str(fileco)+".txt"), "a")
    fileco += 1
    for word,key in overallDict.items():
        f.write(word + ":")
        for doc, value in key.items():
            f.write("d"+str(doc))
            for i in range(6):
                if overallDict[word][doc][i] > 0:
                    f.write(wut[i]+str(overallDict[word][doc][i]))
        f.write("\n")
    f.close()


doc_title = open('titles.txt', 'w')

def index(title, text, docID):
    # title = title.lower()
    text = text.lower()
    titleWords = tokenize(title.lower(), 1)  
    bodyWords = tokenize(text, 1)
    doc_title.write(title.strip()+"\n")

    # Infobox
    infoboxWords = []
    infobox = text.split("{{infobox")
    if len(infobox) > 1:
        infobox = infobox[1].split("}}\n", 1)
        infoboxWords = tokenize(str(infobox[0]), 0)


    # Category
    categoryWords = []
    categories = re.findall(r"\[\[category:(.*)\]\]", text)
    if categories:
        categories = " ".join(categories)
        # print(categories)
        categoryWords = tokenize(categories, 0)
        # print(categoryWords)

    # Links
    linkWords = []
    links = text.split("==external links==")
    if len(links) > 1:
        links = links[1].split("\n")
        linksInfo = ""
        for line in links:
            if line and line[0] == '*':
                linksInfo += line+" "
        linkWords = tokenize(linksInfo, 0)


    # References
    refWords = []
    refs = text.split("==references==")
    if len(refs) > 1:
        refs = refs[1].split("\n")
        refsInfo = ""
        for line in refs:
            if ("[[category" in line) or ("==" in line) or ("defaultsort" in line):
                break
            refsInfo += line+"\n"
        refWords = tokenize(refsInfo, 0)

    for word in titleWords:
        # print("ti ",word)
        if word in overallDict and docID in overallDict[word]:
            overallDict[word][docID][0] += 1
        elif word in overallDict:
            overallDict[word][docID] =[1, 0, 0, 0, 0, 0]
        else:
            overallDict[word] = {docID: [1, 0, 0, 0, 0, 0]}
    
    for word in infoboxWords :
        # print("in ", word)
        if word in overallDict  and docID in overallDict[word]:
            overallDict[word][docID][1] += 1
        elif word in overallDict:
            overallDict[word][docID] =[0, 1, 0, 0, 0, 0]
        else:
            overallDict[word] = {docID: [0, 1, 0, 0, 0, 0]}

    for word in categoryWords:
        # print("ca ", word)
        if word in overallDict  and docID in overallDict[word]:
            overallDict[word][docID][2] += 1

        elif word in overallDict:
            overallDict[word][docID] =[0, 0, 1, 0, 0, 0]
        else:
            overallDict[word]= {docID: [0, 0, 1, 0, 0, 0]}

    for word in linkWords:
        # print(" li ", word)
        if word in overallDict and docID in overallDict[word]:
             overallDict[word][docID][3] += 1
        elif word in overallDict:
            overallDict[word][docID] =[0, 0, 0, 1, 0, 0]
        else:
            overallDict[word] =  {docID: [0, 0, 0, 1, 0, 0]}

    for word in refWords:
        # print("ref ", word)
        if word in overallDict and docID in overallDict[word]:
             overallDict[word][docID][4] += 1
        elif word in overallDict:
            overallDict[word][docID] =[0, 0, 0, 0, 1, 0]
        else:
            overallDict[word]= {docID: [0, 0, 0, 0, 1, 0]}

    for word in bodyWords:
        # print("ref ", word)
        if word in overallDict and docID in overallDict[word]:
             overallDict[word][docID][5] += 1
        elif word in overallDict:
            overallDict[word][docID] = [0, 0, 0, 0, 0, 1]
        else:
            overallDict[word]= {docID: [0, 0, 0, 0, 0, 1]}


    cur = overallDict[word][docID]
    cur[5] = max(cur[5] - cur[4] - cur[3] - cur[2] - cur[1], 0)
    overallDict[word][docID][5] = cur[5] 

wikiDump = sys.argv[1]
# create an XMLReader
begin = datetime.now()
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = ParsingHandler()
parser.setContentHandler(Handler)
for filename in os.listdir(wikiDump):
    parser.parse(os.path.join(wikiDump, filename))
    createMiniIndex()
# print(overallDict)

parse_end = datetime.now()
print("time to parse is ", parse_end-begin)

stats = open(stats, "w")
stats.write(str(total_count) + "\n")
stats.close()

print("DONE!!!")
doc_title.close()
sys.exit()
