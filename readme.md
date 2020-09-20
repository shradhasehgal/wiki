# Wikipedia Search Engine

## Index Creation

The index has ~30 million tokens, split into 3000 files (10,000 tokens each). The tokens are sorted alphabetically in these files. 
The index can be found in `final_index` folder - created with `index.py` and `merge.py`.

I have also stored the first token of each of these files in a file called `mergeWords.txt`.

Titles are stored in 5000 files in `final_index/titles`.


### Method

- After every 10,000 documents, I write to the disk (sorted manner)
- Once inverted index is created in separate files, I merge them
- I merge them by maintaing a heap structure and writing to another set of index files
- 10,000 tokens are written to each final index file
- I also store title of each document and first word of final index files

## Search 

Search utilizes the titles folder and final index folder mentioned above. 

### Method

- I read the first word of each of the final index files into an array
- I lowercase, tokenize, and stem the query 
- I search for the file that has the query term's posting list by binary searching on the aforementioned first words array
- I calculate the tf-idf score based on different weights allotted for t,b,i,r,l,c
- I sort the documents and display the k-best documents