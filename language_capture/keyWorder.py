import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist
import math


class KeyWorder():

    def __init__(self,text=None,filename=None):
        """text is a string that you would like to process
        filename is a file whose text you would like to process
        if filename is specified, text is ignored and filename's text
        is given priority"""
        if filename is not None:
            text = self.opfile(filename)
        else:
            self.text = text

        lem = WordNetLemmatizer()
        self.tokens = [w.lower() for w in word_tokenize(text)]
        words = [word for word in self.tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        filtwords = [w for w in words if w not in stop_words]

        nouns = [lem.lemmatize(w,self.p_o_s(w)) for w in filtwords if self.p_o_s(w) == wordnet.NOUN]
        verbs = [lem.lemmatize(w, self.p_o_s(w)) for w in filtwords if self.p_o_s(w) == wordnet.VERB]
        adj = [lem.lemmatize(w, self.p_o_s(w)) for w in filtwords if self.p_o_s(w) == wordnet.ADJ]
        adv = [lem.lemmatize(w, self.p_o_s(w)) for w in filtwords if self.p_o_s(w) == wordnet.ADV]

        # Using NLTK's built in frequency distribution function
        self.noun_dist = FreqDist(nouns)
        self.verb_dist = FreqDist(verbs)
        self.adj_dist = FreqDist(adj)
        self.adv_dist = FreqDist(adv)
        self.word_dist = FreqDist(nouns+verbs+adj+adv)

    def p_o_s(self,word):
        """returns the part of speech of the word in a form that
        lemmatise() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def get_pos_name(self, word):
        """returns the part of speech of the word as a string"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": "adjective",
                    "N": "noun",
                    "V": "verb",
                    "R": "adverb"}
        return tag_dict.get(tag, "other")

    def opfile(self,filename):
        text = ""
        f = open(filename, 'r')
        for line in f:
            text += line.strip()
            text += " "
        return text

    """top_words outputs key word lists for the text, in
    the form of a list of (word,frequency) tuples. 
    """

    def top_words(self, num=5, percent=None, pos = False):
        """pos=True means this method returns an ordered list of all the
         parts of the speech of all the common words in the word distribution
         You can either specify num which is the number of key words you are
         looking for, or you can specify percent which is safer as it returns
         a percentage of the key words"""
        if (num is not None) and (num > len(self.word_dist)):
            num = len(self.word_dist)-1  # Catch errors when num exceeds the total number of words
        if percent is not None:  # The largest option of num or percent is taken
            tmp = math.floor((float(len(self.word_dist)) / 100) * percent)  # Number of key words from % of total words
            if num is not None:
                if tmp > num:
                    num = tmp
                # If the specified num is greater than tmp then it is unchanged
            else:
                num = tmp  # If not num is None
        top = self.word_dist.most_common(num)
        top = [t for t in top if (len(t[0]) > 2)]  # No words of length one
        if pos:
            pos_names = [self.get_pos_name(w[0]) for w in top]
            return top, pos_names
        else:
            return top




