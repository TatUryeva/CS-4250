#-------------------------------------------------------------------------
# AUTHOR: Tatsiana Uryeva
# FILENAME: db_connection
# SPECIFICATION: database functions
# FOR: CS 4250 - Assignment #2
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
from psycopg2.extras import RealDictCursor
import string

def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    DB_NAME = "Database"
    DB_USER = "postgres"
    DB_PASS = "password"
    DB_HOST = "localhost"
    DB_PORT = "5433"
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        return conn
    except:
        print("Database not connected successfully")

def createCategory(cur, catId, catName):

    # Insert a category in the database
    # --> add your Python code here
    sql = "Insert into \"Categories\" (id_cat, name) Values (%s, %s);"
    recset = [catId, catName]
    cur.execute(sql, recset)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    sql = "Select id_cat from \"Categories\" where \"name\" = %s;"
    recset = [docCat]
    cat_id = cur.execute(sql, recset)

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    sql = "Insert into \"Documents\" (doc, text, title, num_chars, date, cat_id) Values (%s, %s, %s, %s, %s, %s);"
    recset = [docId, docText, docTitle, len(docText.strip(string.punctuation)), docDate, cat_id]
    cur.execute(sql, recset)

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    sql = "Select term from \"Terms\";"
    cur.execute(sql)
    terms = cur.fetchall()
    #print(terms)
    text = docText.lower().split()
    #print(text)
    for i, word in enumerate(text):
        text[i] = word.strip(string.punctuation)
        if text[i] not in terms:
            sql = "Insert into \"Terms\" (term, num_chars) Values (%s, %s);"
            recset = [text[i], len(text[i])]
            cur.execute(sql, recset)

        sql = "Insert into \"Document-Term\" (doc_id, term, term_count) Values (%s, %s, %s);"
        recset = [docId, text[i], 0]
        cur.execute(sql, recset)
#        else
#            sql = "Select term_count from Document-Term where doc_id = %s and term = '%s'"
#            recset = [docId, text[i]]
#            term_count = cur.execute(sql)
#            term_count = term_count + 1
#            sql = "Insert into Document-Term (doc_id, term, term_count) Values (%s, '%s', %s)"
#            recset = [docId, text[i], term_count]
#            cur.execute(sql)

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    for i, word in enumerate(text):
        sql = "Select term_count from \"Document-Term\" where doc_id = %s and term = %s;"
        recset = [docId, text[i]]
        cur.execute(sql, recset)
        term_count = cur.fetchone()
        term_count = term_count[0]
        term_count = term_count + 1
        sql = "Update \"Document-Term\" set term_count = %s where doc_id = %s and term = %s;"
        recset = [term_count, docId, text[i]]
        cur.execute(sql, recset)  

def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    sql = "Delete from \"Document-Term\" where doc_id = %s;"
    recset = [docId]
    cur.execute(sql, recset)
    
    sql = "Select term from \"Terms\";"
    cur.execute(sql)
    terms = cur.fetchall()
    sql = "Select term from \"Document-Term\";"
    cur.execute(sql)
    occurrences = cur.fetchall()
    for term in terms:
        if term not in occurrences:
            sql = "Delete from \"Terms\" where term = %s;"
            recset = [term]
            cur.execute(sql, recset)

    # 2 Delete the document from the database
    # --> add your Python code here
    sql = "Delete from \"Documents\" where doc = %s;"
    recset = [docId]
    cur.execute(sql, recset)

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    sql = "Delete from \"Documents\" where doc = %s;"
    recset = [docId]
    cur.execute(sql, recset)

    # 2 Create the document with the same id
    # --> add your Python code here
    sql = "Insert into \"Documents\" (doc, text, title, num_chars, date, cat_id) Values (%s, '%s', '%s', '%s',  %s);"
    recset = [docId, docText, docTitle, docDate, cat_id]
    cur.execute(sql, recset)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    sql = "Select term from \"Terms\";"
    cur.execute(sql)
    terms = cur.fetchall()
    #print("terms")
    #print(terms, "\n")
    sql = "Select term, title, term_count from \"Document-Term\" inner join \"Documents\" on doc_id = doc;"
    cur.execute(sql)
    occurrences = cur.fetchall()
    #print("occurrences")
    #print(occurrences, "\n")
    inverted_index = dict()
    for i, term in enumerate(terms):
        inverted_index[term[0]] = list()
        for ii, occurrence in enumerate(occurrences):
            if occurrence[0] == term[0]:
                #print(occurrence, end = " ")
                #print(occurrence[1], end = " ")
                #print(occurrence[2], end = "\n")
                inverted_index[term[0]].append({occurrence[1]:occurrence[2]})
    #print("inverted_index")
    #print(inverted_index)
    return inverted_index
