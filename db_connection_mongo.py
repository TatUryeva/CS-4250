#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #3
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
#import pymongo
from pymongo import MongoClient
import datetime
import string

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = MongoClient(host = "localhost", port = 27017)
    db = client.documents
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary indexed by term to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    text = docText.lower().split()
    termDict = {}
    
    for term in text:
        term = term.strip(string.punctuation)
        if term not in termDict:
            termDict[term] = 1
        else:
            termDict[term] = termDict[term] + 1            

    # create a list of objects to include full term objects. [{"term", count, num_char}]
    # --> add your Python code here            
    termObjList = []
    
    for term in termDict:
        termObj = {"term":term, "term_count":termDict[term]}
        termObjList.append(termObj)

    # produce a final document as a dictionary including all the required document fields
    # --> add your Python code here
    doc = {"_id":docId, "text":docText, "title":docTitle, "num_chars":len(docText.replace(string.punctuation, "")),
           "date":datetime.datetime.strptime(docDate,"%Y-%m-%d"), "category":docCat, "terms":termObjList}

    # insert the document
    # --> add your Python code here
    result = col.insert_one(doc)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    documents.delete_one({"_id":docID})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here
    col.delete_one({"_id":docId})

    # Create the document with the same id
    # --> add your Python code here
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    pipeline = [{"$unwind":{"path":"$terms"}}]
    output = col.aggregate(pipeline)
    docs = list(output)
    indexDict = {}
    for doc in docs:
        if doc["terms"]["term"] not in indexDict:
            indexDict[doc["terms"]["term"]] = {doc["title"]:doc["terms"]["term_count"]}
        else:
            indexDict[doc["terms"]["term"]][doc["title"]] = doc["terms"]["term_count"]
          
    return indexDict
