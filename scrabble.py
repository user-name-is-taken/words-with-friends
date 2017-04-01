""" remember, "." is the wildcard
"""
from WWF_DDC import *

def make_words_list():
    """Reads lines from a file and builds a dictionary with word[]:'' pairs."""
    word_list=list()
    fin = open('words.txt','r')
    for line in fin:
        word = line.strip()
        word_list.append(word)
    return word_list

def prompt_seqs():
    """prompts for multiple seqences"""
    message="""\nEnter a sequence to search for.\nUse '.' as a wildcard.
Starting a sequence with '+' returns words that start with the sequence.
Ending a sequence with '+' returns words that end with the sequence.
Enter x to stop inputting sequences."""
    imps=list()
    inp=input(message)
    while inp!='x':
        imps.append(inp)
        inp=input(message)
    return imps


def make_histo(st):
    """makes a {letter:freq} histogram"""
    return {i:st.count(i) for i in set(st)}

def uses_only(given_letters,word_letters,is_scrabble=True):
    """determines if word_letters contains only the elements in given_letters.
there's a bug here"""
    if is_scrabble:given_letters=given_letters+"++"
    histG=make_histo(given_letters)#in a larger program, this would be global.
    histW=make_histo(word_letters)
    required_wildcards=0
    for KW,W in histW.items():
        if W>histG.get(KW,0):
            required_wildcards+=W-histG.get(KW,0)
    return histG.get(".",0)>=required_wildcards

def letters_on_board(limit,given_letters):
    """removes sequences that contain letters not in given_letters
from limit"""
    return {i for i in limit if uses_only(given_letters,i)}
def scrabbleHand():
    """prompts the user for their letters, then the board letters, then
finds the inputs"""
    letters=input("Enter the letters in your scrabble hand. "+
                  "Enter '.' for wildcard letters.\nEnter x to exit")
    if letters =="x":return False
    seqs=prompt_seqs()
    delimitedSeqs={i:ff.new_scrabble(i) for i in seqs}
    for i in delimitedSeqs:
        print(i)
        #print(delimitedSeqs)
        print(list(filter(lambda x: uses_only(letters+i,x[1]),delimitedSeqs[i])))
    return True    

def main():
    global d
    global ff
    d=make_words_list()
    ff=Regex_list(d)#imported
    while scrabbleHand():
        pass


if __name__=="__main__":
    main()
    
