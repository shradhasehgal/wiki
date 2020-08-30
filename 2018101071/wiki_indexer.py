import sys
import xml.sax
import Stemmer
from nltk.corpus import stopwords 
import re
from datetime import datetime
import multiprocessing 

total_count = 0
articles = []

class Article():
    def __init__(self, x, y, z):
        self.title = x
        self.text = y
        self.docID = z

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
            articles.append(Article(self.title, self.text, self.docID))
            # index(articles[])
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
stemmer = Stemmer.Stemmer("english")
overallDict = {}

def tokenize(text, all):
    words = re.split(r'[^a-z0-9]+', text)
    filtered = []
    global total_count
    if all:
        total_count += len(words)

    for w in words: 
        if w not in stop_words:
            if w not in stems:
                if len(w) > 0:
                    stemmed_w = stemmer.stemWord(w)
                    filtered.append(stemmed_w)
                    stems[w] = stemmed_w
            else:
                filtered.append(stems[w])

    return filtered

def index(article):
    title = article.title.lower()
    text = article.text.lower()
    docID = article.docID
    titleWords = tokenize(title, 1)  
    bodyWords = tokenize(text, 1)
    
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

    overallDict = {}
    addToList(titleWords, 0, overallDict)
    addToList(infoboxWords, 1, overallDict)
    addToList(categoryWords, 2, overallDict)
    addToList(linkWords, 3, overallDict)
    addToList(refWords, 4, overallDict)
    addToList(bodyWords, 5, overallDict)
    return overallDict, docID

def addToList(words, index, overallDict):
    for word in words:
        if word in overallDict:
            overallDict[word][index] += 1
        else:
            overallDict[word] = [0, 0, 0, 0, 0, 0]
            overallDict[word][index] = 1
        

wikiDump = sys.argv[1]
begin = datetime.now()
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = ParsingHandler()
parser.setContentHandler(Handler)
parser.parse(wikiDump)

pool = multiprocessing.Pool()
outputs = pool.map(index, articles)
# print(outputs[0])

overallDict = {}
for article in outputs:
    for key,value in article[0].items():
        if key in overallDict and article[1] in overallDict[key]:
            for index in range(6):
                overallDict[key][article[1]][index] += value[index]
        elif key in overallDict:
            overallDict[key][article[1]] = value
        else:
            overallDict[key] = {article[1]: value}

# print(overallDict)
wut = ['t', 'i', 'c', 'l', 'r', 'b']
f = open("index.txt", "a")
for word,post in overallDict.items():
    f.write(word + ":")
    for doc, value in post.items():
        f.write("d"+str(doc))
        for i in range(6):
            if overallDict[word][doc][i] > 0:
                f.write(wut[i]+str(overallDict[word][doc][i]))
    f.write("\n")
f.close()

parse_end = datetime.now()
print("time to parse is ", parse_end-begin)

stats = open("invertedindex_stat.txt", "a")
stats.write(str(total_count) + "\n")
stats.write(str(len(overallDict)))
