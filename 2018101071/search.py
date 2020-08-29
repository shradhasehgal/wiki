import sys
searchStr = sys.argv[1]

searchStr = searchStr.lower()
words = {}

if ":" in searchStr:
    temps = searchStr.split(":")
    for i in range(1, len(temps)):
        if i == len(temps) -1:
            words[temps[i-1][-1]] = temps[i]
        else:
            words[temps[i-1][-1]] = temps[i][: -2]

else:
    words['a'] = searchStr

indexRead = open("index.txt", "r")
termPost = {}

for line in indexRead:
    readLine = line.split(":")
    termPost[readLine[0]] = readLine[1]


for key, val in words.items():
    searchTerms = val.split(' ')
    for term in searchTerms:
        if key == "a":
            if term in termPost:
                print("\nSearch term: "+ term, end='')
                posting = termPost[term]
                i = 0
                while i < len(posting):
                    if posting[i] == 'd':
                        print("\nD", end='')
                        i += 1
                        while posting[i].isdigit():
                            print(posting[i], end='')
                            i += 1
                        print(": ", end='')
                    print(posting[i], end='')
                    i +=1


                        
        else:
            if term in termPost and key in termPost[term]:
                print("\nSearch term: "+ term, end='')
                posting = termPost[term]
                i = 0
                while i < len(posting):
                    if posting[i] == 'd':
                        print("\nDocID ", end='')
                        i += 1
                        while posting[i].isdigit():
                            print(posting[i], end='')
                            i += 1
                        print(": ", end='')
                    print(posting[i], end='')
                    i +=1