# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object
# ########################################

# from lib2to3.pgen2.tokenize import tokenize
from operator import index

from matplotlib import legend
import cs547
import os     
from PorterStemmer import *

MY_NAME = "Parth Patel"
MY_ANUM  = 661591670 # put your WPI numerical ID here
MY_EMAIL = "pdpatel@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [ 
    ]

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs547.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        num_files_indexed = 0
               
        all_files = os.listdir(base_path)
        for i in all_files:
            self._documents.append(i[:-4]) 
            text = open(base_path + i,'r').read()  
            tokenize = Index.tokenize(index, text)
            stemming = Index.stemming(index,tokenize)
            for j in stemming:
                if j in self._inverted_index:
                    if i[:-4] in self._inverted_index[j]:
                        continue
                    self._inverted_index[j].append(i[:-4])
                else:
                    self._inverted_index[j] = [i[:-4]]
            num_files_indexed+=1 
        
        # PUT YOUR CODE HERE
        return num_files_indexed

    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        # PUT YOUR CODE HERE
        text = text.lower()
        for i in range(len(text)):
            if text[i].isdigit() or text[i].isalpha():
                
                continue
            else:
                text = text[:i] + ' ' + text[i+1:]

        tokens = text.split()

        return tokens

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        stemmed_tokens = []
        # PUT YOUR CODE HERE
        for i in tokens:
            p = PorterStemmer()
            stemmed_tokens.append(PorterStemmer.stem(p,i, 0, len(i)-1))
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        results = []
        # # PUT YOUR CODE HERE
        t = text.split()
        if len(t) == 1:
            tokenize = Index.tokenize(index, t[0])
            stemming = Index.stemming(index,tokenize)
            temp = []
            for i in stemming:
                temp.append(self._inverted_index[i])
            results = set.intersection(*[set(p) for p in temp])
            
        elif len(t) == 3:
            if t[1]=='OR':
                tokenize = Index.tokenize(index, t[0])
                stemming = Index.stemming(index,tokenize)
                temp = []
                
                for i in stemming:
                    temp.append(self._inverted_index[i])

                temp1 = list(set.intersection(*[set(p) for p in temp]))
                
                tokenize = Index.tokenize(index, t[2])
                stemming = Index.stemming(index,tokenize)
                temp=[]
                
                for i in stemming:
                    temp.append(self._inverted_index[i])
                
                temp2 = list(set.intersection(*[set(p) for p in temp]))
                results = list(set(temp1 + temp2))
                
            elif t[1]=='AND':
                tokenize = Index.tokenize(index, t[0])
                stemming = Index.stemming(index,tokenize)
                temp = []
              
                for i in stemming:
                    temp.append(self._inverted_index[i])
                temp1 = list(set.intersection(*[set(p) for p in temp]))
                tokenize = Index.tokenize(index, t[2])
                stemming = Index.stemming(index,tokenize)
                temp=[]
               
                for i in stemming:
                    temp.append(self._inverted_index[i])
                temp2 = list(set.intersection(*[set(p) for p in temp]))
                results = list(set(temp1) & set(temp2))



            
        return results
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    num_files = index.index_dir('data/')
    print("indexed %d files" % num_files)
    for term in ('Parth', 'Mark', 'sherman', 'Mark OR sherman', 'Mark AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)


