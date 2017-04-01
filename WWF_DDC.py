#import this
"""This is the data definition class for regex_list.
regex_list takes a list of strings and makes it searchable.
Searchable meaning you can find which elements in the list have a pattern.
you could add the '+' to the add word.
    Remember seq is a subset of word
"""
import itertools

class Regex_list(object):
    """this will make your word list searchable.
Note, It will also loose the original order of the list."""
    def __init__(self, lis):
        assert hasattr(lis,"__iter__")
        self.all_words = set()
        self.search_dict = dict()
        for word in set(lis):self.add_word(word)
        #self.calculateFreqs()
        
    def add_word(self,word):
        """this will add a word to the search_dict
search dict is of the form: {letter:{nextletter:{(index,word)}}}
"""
        assert type(word) is str#or isinstance(word,str)
        assert word not in self.all_words#already have it!
        assert "+" not in word
        if "." in word: print("you shouldn't have a '.' but suit yourself")
        self.all_words.add(word)
        word="+"+word+"+"#helps find words that start/end with the pattern
        #doesn't interfere with patterns that dont have "+" at start/end
        for index,val in enumerate(word[:-1]):
            next_letter = self.search_dict.setdefault(val,dict())
            words_list = next_letter.setdefault(word[index+1],set())#object modification
            words_list.add((index,word))#object modifification
            
    def find_matches(self,seq):
        """finds all the words in the list with this sequence.
Uses '.' as wildcard.
(remember it only finds exact matches)"""
        assert len(seq)>=2    
        s_d = self.search_dict
        setsList =[]
        finalSetPairs=list()#test
        while seq[-1]=='.' and len(seq)>2:#problem
            """not solved by if index+1=='.' because there's no [letter][''] for word endings in self.search_dict.
#without this, .f. wouldn't find (0,"of"), because the L_m in the seq[index+1]=="." if wouldn't include it.
#the len>2 is needed to find sequences matches that are like "f."
despite these improvements, 1 letter sequences still won't be found. but they're obvious...
worst case, just search self.all_words for them
"""
            seq = seq[:-1]
        for index,letter in enumerate(seq[:-1]):
            if not(letter=="." and seq[index+1]=="."):#no point if they all match...
                if letter==".":
                    L_m = set.union(*(i.get(seq[index+1],set()) for i in s_d.values()))
                    #.get is important here. not all is have i[seq[index+1]]
                elif seq[index+1]==".":
                    L_m = set.union(*s_d[letter].values())
                else:
                    L_m = s_d[letter].get(seq[index+1],{})#this is a set.
                    #not using s_d.get could cause errors here...
                #L_m==letter_matches
                setsList.append({(i-index,word) for i,word in L_m})
                finalSetPairs.append([index,L_m])#test
                #finding a workaround for this would be a good idea
                #so you don't have to do so many i-index operations
                #maybe switch it to an add and perform it iteratively
                #if you do letter freq you cant do the add intersect
                #if you do the add intersect you're add to the intersected set obvi
        s= set.intersection(*setsList)
        s2=self.fast_intersection(finalSetPairs)
        print(len(s),"  ",len(s2))
        return s
    def fast_intersection(self,finalSetPairs):
        """needs work
ff.find_matches("g..rs")
really not sure what the problem is...
theres a string of enumerates here that are complicated but
provid speed
"""
        sorted_pairs=sorted(finalSetPairs,key=lambda x: len(x[1]))
        offset=sorted_pairs[0][0]
        thisSet=sorted_pairs[0][1]
        for index,pair in enumerate(sorted_pairs[1:]):        
            offset=(pair[0]-offset)#sorted_pairs[index-1][0])
            thisSet={(i+offset,word) for i,word in thisSet}
            thisSet.intersection_update(pair[1])            
        return thisSet


    def find_scrabble_strings(self,seq):
        """you need to test this.
Finds all combinations of seq that you could play on in scrabble
delimited with '.' (meaning the spaces on the board are '.'
"""
        listSeqs=seq.split(".")
        seqSets=set()
        for comb in itertools.combinations(range(len(listSeqs)),2):
            MIN=min(comb)
            MAX=max(comb)
            seqSets.add((MIN>0)*"+"+".".join(listSeqs[MIN:MAX+1])+(MAX<(len(listSeqs)-1))*"+")
        seqSets=filter(lambda x:len(x.replace("+",""))>1,seqSets)
        #at least 2 searchable characters
        seqSets=filter(lambda x:len(x.replace(".","").replace("+",""))>=1,seqSets)
        #at least 1 actual letter
        return set(seqSets)
    
    def new_scrabble(self,seq):
        """finds the scrabble matches
for example in scrabble, "of" would fit +.f..g.k+
"""
        assert "+" not in seq[1:-1]
        setsList=list()
        seqs=self.find_scrabble_strings(seq)
        for seq in seqs:
            setsList.append(self.find_matches(seq))
        return set.union(*setsList)                
            
if __name__=="__main__":
    from scrabble import make_words_list
    d = make_words_list()
    ff = Regex_list(d)
    L = ff.new_scrabble(".f")
    #with "..f" (-1,'of')
