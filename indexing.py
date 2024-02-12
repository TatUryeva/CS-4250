#-------------------------------------------------------------------------
# AUTHOR: Tatsiana Uryeva
# FILENAME: indexing.py
# SPECIFICATION: output a tf-idf document-term matrix
# FOR: CS 4250 - Assignment #1
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append(row[0])

#Conducting stopword removal. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {'i ', 'my ', 'she ', 'her ','they ', 'their ', 'and ', 'or '}
docs = []
for i, document in enumerate(documents):
    docs.append(document.split(' '))

for i, document in enumerate(documents):
    documents[i] = document.lower()
    for ii, stopWord in enumerate(stopWords):
        documents[i] = documents[i].replace(stopWord, '')

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {'love':['love', 'loves', 'loved'], 'cat':['cat', 'cats'], 'dog':['dog', 'dogs']}
for i, document in enumerate(documents):
    document = document.split(' ')
    for ii, stem in enumerate(stemming):
        for iii, word in enumerate(document):
            if word in stemming['love']:
              documents[i] = documents[i].replace(word, 'love')
            elif word in stemming['cat']:
              documents[i] = documents[i].replace(word, 'cat')
            elif word in stemming['dog']:
              documents[i] = documents[i].replace(word, 'dog')

#Identifying the index terms.
#--> add your Python code here
terms = ['love', 'cat', 'dog']
P = []
for i, term in enumerate(terms):
       P.append(0)
       for ii, document in enumerate(documents):
              if term in document.split(' '):
                     #P = P + 1
                     P[i] = P[i] + 1

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = []
for i, document in enumerate(documents):
       docTermMatrix.append([])
       for ii, term in enumerate(terms):
              tf = documents[i].count(term)/len(docs[i])
              idf = math.log10(len(documents)/P[ii])
              docTermMatrix[i].append(tf*idf)

#Printing the document-term matrix.
#--> add your Python code here
print('\t', end='\t')
for term in terms:
    print(term, end = '\t')
print()
for i, document in enumerate(documents):
   print('document' + str(i), end = '\t')
   for ii, term in enumerate(terms):
      print(str(round(docTermMatrix[i][ii], 2)), end = '\t')
   print()
