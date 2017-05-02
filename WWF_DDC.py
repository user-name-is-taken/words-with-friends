#import this
#change find_matches to freq analysis --> intersection to remove unions
"""This is the data definition class for regex_list.
regex_list takes a list of strings and makes it searchable.
Searchable meaning you can find which elements in the list have a pattern.
you could add the '+' to the add word.
    Remember seq is a subset of word
http://www.clips.ua.ac.be/tutorials/python-performance-optimization
"""
import itertools
import timeit

def timer(val):
    """times find_matches.
proves that the unions are the slowest thing now,because:
timer("e."*100) takes about the same time as timer(("e."*100)+"z")
and the "z" reduces a ton of intersections.
"""
    start=timeit.default_timer()
    ff.find_matches(val)
    stop=timeit.default_timer()
    return stop-start

class Regex_list(object):
    """this will make your word list searchable.
Note, It will also loose the original order of the list."""
    def __init__(self, lis):
        assert hasattr(lis,"__iter__")
        self.all_words = set()
        self.search_dict = dict()
        self.total_len=0
        for word in set(lis):self.add_word(word)
        self.maxSortLen=25
        
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
        self.total_len+=len(word)-1
        for index,val in enumerate(word[:-1]):
            next_letter = self.search_dict.setdefault(val,dict())
            words_list = next_letter.setdefault(word[index+1],set())#object modification
            words_list.add((index,word))#object modifification

    def __remove_leading_n_trailing_dots__(self,seq):
        """removing these will add matches to the result that the user
probably wants"""
        leading=next(i for i in range(len(seq)) if seq[i]!='.')
        trailing=next(i for i in range(len(seq)-1,0,-1) if seq[i]!='.')
        return seq[leading:trailing+1]
            
    def find_matches(self,seq):
        """finds all the words in the list with this sequence.
Uses '.' as wildcard.
(remember it only finds exact matches)
ff.find_matches("+h..lo+")
"b..ad"?"""
        assert len(seq.replace(".",""))>=2
        seq=self.__remove_leading_n_trailing_dots__(seq)
        s_d = self.search_dict
        matchesLfun=self.__seqMatches__(seq)
        SortedVals=list(enumerate(seq[:-1]))#in a long seq, this is the slow part
        if len(seq)<self.maxSortLen:
            Key=self.__KeyMaker__(seq)
            SortedVals=sorted(SortedVals,key=Key)
        else:
            SortedVals=SortedVals[::-1]
        #this line would be good, if I had a limit on word length
        #and not just an intersection"""
        s2=set.union(*matchesLfun(SortedVals[0][0]))#can't have .. at 0 pos and > 15 chars
        for index,enumer in enumerate(SortedVals[1:]):
            letterIndex,letter=enumer
            if not(letter=="." and seq[letterIndex+1]=="."):#no point if they all match...
                sL=[]
                for i in matchesLfun(letterIndex):
                    sL.append(self.__fast_intersection__(s2,i,SortedVals[index][0],letterIndex))
                    #note: sorted_pairs[1:][index-1][0]== sorted_pairs[index][0]
                s2=set.union(*sL)
                if len(s2)==0:
                    #print('here')
                    return set()
        return s2

    def __fast_intersection__(self,firstSet,secondSet,firstSetIndex,secondSetIndex):
        """This intersects the two sets using the addition to make it faster
"""
        offset=secondSetIndex-firstSetIndex
        #note: sorted_pairs[1:][index-1][0]== sorted_pairs[index][0]
        firstSet={(i+offset,word) for i,word in firstSet}
        return firstSet.intersection(secondSet)

    def __KeyMaker__(self,seq):
        matchesLfun=self.__seqMatches__(seq)#this is why the internal function is needed.
        def key(enumer):
            """was seems to be wrong"""
            index=enumer[0]
            if seq[index]=="." and seq[index+1]==".":return self.total_len
            return sum((len(i) for i in matchesLfun(index)))
        return key
    
    def __seqMatches__(self,seq):
        s_d=self.search_dict
        def matchesSetList(index):
            """
This looks up the bigram patterns of seq[index:index+1]
returns a list of all the sets that match the pattern
at this index. Doesn't handle '..' situations nicely."""
            #.get is important here. not all i's have i[seq[index+1]]

            #this is a set.
            #not using s_d.get could cause errors here...
            #note: sorted_pairs[1:][index-1][0]== sorted_pairs[index][0]
            #print("in matchesSetList ",seq[index],seq[index+1])
            MSL=""
            if seq[index]==".":
                MSL= [i.get(seq[index+1],set()) for i in s_d.values()]
            elif seq[index+1]=='.':
                MSL= s_d.get(seq[index],dict()).values()
            elif seq[index]=="." and seq[index+1]==".":
                MSL= ".."
            else:
                MSL= [s_d.get(seq[index],dict()).get(seq[index+1],set()),]
            if index>self.maxSortLen:
                MSL=list(set(filter(lambda x:x[0]>=index,x)) for x in MSL)
            return MSL
        return matchesSetList


    def __find_scrabble_strings__(self,seq):
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
        #assert len(seq)<20
        setsList=[]
        seqs=self.__find_scrabble_strings__(seq)
        seqs.add(seq)
        for seq in seqs:
            setsList.append(self.find_matches(seq))
        return set.union(*setsList)


if __name__=="__main__":
    from scrabble import make_words_list
    d = make_words_list()
    ff = Regex_list(d)
    #L = ff.new_scrabble(".f")
    #with "..f" (-1,'of')
