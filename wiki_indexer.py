import sys
import xml.sax
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords 
import re
from datetime import datetime

class ParsingHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.text = ""
        self.title = ""
        self.docID = 0
        self.tag = ""
    
    def startElement(self, tag, attributes):
        self.tag = tag

    def endElement(self, tag):
        if tag == "page":
            index(self.title, self.text, self.docID)
            self.title = ""
            self.text = ""
            self.docID += 1

    def characters(self, content):
        if self.tag == "title":
            self.title += content
        elif self.tag == "text":
            self.text += content

stop_words = set(stopwords.words('english')) 
stems = {}
stemmer = SnowballStemmer("english")
overallDict = {}

def tokenize(text):
    words = re.split(r'[^a-z0-9]+', text)
    filtered = []
    for w in words: 
        if w not in stop_words:
            if w not in stems:
                if len(w) > 0:
                    stemmed_w = stemmer.stem(w)
                    filtered.append(stemmed_w)
                    stems[w] = stemmed_w
            else:
                filtered.append(stems[w])

    return filtered

def index(title, text, docID):
    title = title.lower()
    text = text.lower()
    titleWords = tokenize(title)  
    bodyWords = tokenize(text)
    
    # Infobox
    infoboxWords = []
    infobox = text.split("{{infobox")
    if len(infobox) > 1:
        infobox = infobox[1].split("}}", 1)
        infoboxWords = tokenize(str(infobox[0]))


    # Category
    categoryWords = []
    categories = re.findall(r"\[\[category:(.*)\]\]", text)
    if categories:
        categories = " ".join(categories)
        # print(categories)
        categoryWords = tokenize(categories)
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
        linkWords = tokenize(linksInfo)


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
        refWords = tokenize(refsInfo)

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
            overallDict[word][docID] =[0, 0, 0, 0, 0, 1]
        else:
            overallDict[word]= {docID: [0, 0, 0, 0, 0, 1]}
        

wikiDump = sys.argv[1]
# create an XMLReader
begin = datetime.now()
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = ParsingHandler()
parser.setContentHandler(Handler)
parser.parse(wikiDump)
# print(overallDict)
# overallDict = {'4529332': {19796: [0, 0, 0, 0, 0, 1]}, 'tardisk': {19796: [0, 0, 0, 0, 0, 4]}, 'tardishir': {19796: [0, 0, 0, 0, 0, 2]}, '23639332': {19796: [0, 0, 0, 0, 0, 2]}, '20100223004654': {19796: [0, 0, 0, 0, 0, 1]}, 'tardiscam': {19796: [0, 0, 0, 0, 0, 1]}, 'retardi': {19796: [0, 0, 0, 0, 0, 3]}, '10940401': {19796: [0, 0, 0, 0, 0, 1]}, '6705231': {19796: [0, 0, 0, 0, 0, 1]}, '35801': {19796: [0, 0, 0, 0, 0, 1]}, 'wabac': {19796: [0, 0, 0, 0, 0, 1]}, 'hammerspac': {19796: [0, 0, 0, 0, 0, 1]}}

wut = ['t', 'i', 'c', 'l', 'r', 'b']
f = open("index.txt", "a")
for word,key in overallDict.items():
    f.write(word + ":")
    for doc, value in key.items():
        f.write(str(doc))
        for i in range(6):
            # print(overallDict[word][doc])
            if overallDict[word][doc][i] > 0:
                f.write(wut[i]+str(overallDict[word][doc][i]))
        f.write('|')
    f.write("\n")
f.close()

parse_end = datetime.now()
print("time to parse is ", parse_end-begin)


# print(stop_words)

