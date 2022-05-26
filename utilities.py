# some useful functions

import os
import nltk
import re
from xml.etree import ElementTree

def load_entire_directory(directory_path):
    files = os.listdir(directory_path)
    corpus = {}
    for f in files:
        if f[0] != ".":
            file = open(directory_path + '/' + f)
            fname = re.sub("\..*$", "", f)
            corpus[fname] = file.read()
            file.close()
    return corpus

def read_and_tokenize(filename):
    myfile = open('corpora/' + filename)
    raw_string = myfile.read()
    word_list = nltk.word_tokenize(raw_string)
    return word_list


class ListTable(list):
    def _repr_html_(self):
        html = ["<table style= 'border: 1px solid black;''>"]
        for row in self:
            html.append("<tr>")
            for col in row:
                html.append("<td align='left' style='border: .5px solid gray;''>{0}</td>".format(col))
            
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

def bruces_twitter_tokenizer(text):
    import re
    
    def is_contraction(the_text):
        contraction_patterns = re.compile(r"(?i)(.)('ll|'re|'ve|n't|'s|'m|'d)\b")
        return contraction_patterns.search(the_text)
    
    punctuation_class = r"([\.\-\/&\";:\(\)\?\!\]\[\{\}\*#])"
    
    # eliminate_urls
    text = re.sub(r"http\S*", "", text)
    
    # elimintate hashtags, user mentionds
    text = re.sub(r"#\S*", "", text)
    text = re.sub(r"@\S*", "", text)
    
    # Separate most punctuation at end of words

    text = re.sub(r"(\w)" + punctuation_class, r'\1 \2 ', text)
    
    # Separate most punctuation at start of words
    text = re.sub(punctuation_class + r"(\w)", r'\1 \2', text)
    
    # Separate punctuation from other punctuation
    text = re.sub(punctuation_class + punctuation_class, r'\1 \2 ', text)
    
    # Put spaces between + and = signs and digits. Also %s that follow a digit, $s that come before a digit
    text = re.sub(r"(\d)([+=%])", r'\1 \2 ', text)
    text = re.sub(r"([\$+=])(\d)", r'\1 \2', text)
    
    # Separate commas if they're followed by space.
    # (E.g., don't separate 2,500)
    text = re.sub(r"(,\s)", r' \1', text)
    
    #when we have two double quotes make it 1.
    #
    text = re.sub("\"\"", "\"", text)

    # Separate leading and trailing single and double quotes .
    text = re.sub(r"(\'\s)", r' \1', text)
    text = re.sub(r"(\s\')", r'\1 ', text)
    text = re.sub(r"(\"\s)", r' \1', text)
    text = re.sub(r"(\s\")", r'\1 ', text)
    text = re.sub(r"(^\")", r'\1 ', text)
    text = re.sub(r"(^\')", r'\1 ', text)
    text = re.sub(r"('\'$)", r' \1', text)
    text = re.sub(r"('\"$)", r' \1', text)

    #Separate parentheses where appropriate
    text = re.sub(r"(\)\s)", r' \1', text)
    text = re.sub(r"(\s\()", r'\1 ', text)

    # Separate periods that come before newline or end of string.
    text = re.sub('\. *(\n|$)', ' . ', text)
    
    # separate single quotes in the middle of words
    # text = re.sub(r"(\w)(\')(\w)", r'\1 \2 \3', text)
    
    # separate out 's at the end of words
    text = re.sub(r"(\w)(\'s)(\s)", r"\1 s ", text)
    split_text = text.split()
    
    return split_text

def bruces_alpha_only(text, stem_text=False, alpha_only=True, lower_case=True):
    import re
    from nltk import stem  # @UnresolvedImport
    
    def is_contraction(the_text):
        contraction_patterns = re.compile(r"(?i)(.)('ll|'re|'ve|n't|'s|'m|'d)\b")
        return contraction_patterns.search(the_text)

    def return_alpha_only (ltext):
        return [w for w in ltext if (len(w) > 0) and (w.isalpha() or w[0]=='<' or is_contraction(w))]
    
    stemmer = stem.PorterStemmer()
    if lower_case:
        text = text.lower()
    punctuation_class = r"([\.\-\/&\";:\(\)\?\!\]\[\{\}\*#])"
    
    # Separate most punctuation at end of words

    text = re.sub(r"(\w)" + punctuation_class, r'\1 \2 ', text)
    
    # Separate most punctuation at start of words
    text = re.sub(punctuation_class + r"(\w)", r'\1 \2', text)
    
    # Separate punctuation from other punctuation
    text = re.sub(punctuation_class + punctuation_class, r'\1 \2 ', text)
    
    # Put spaces between + and = signs and digits. Also %s that follow a digit, $s that come before a digit
    text = re.sub(r"(\d)([+=%])", r'\1 \2 ', text)
    text = re.sub(r"([\$+=])(\d)", r'\1 \2', text)
    
    # Separate commas if they're followed by space.
    # (E.g., don't separate 2,500)
    text = re.sub(r"(,\s)", r' \1', text)
    
    #when we have two double quotes make it 1.
    #
    text = re.sub("\"\"", "\"", text)

    # Separate leading and trailing single and double quotes .
    text = re.sub(r"(\'\s)", r' \1', text)
    text = re.sub(r"(\s\')", r'\1 ', text)
    text = re.sub(r"(\"\s)", r' \1', text)
    text = re.sub(r"(\s\")", r'\1 ', text)
    text = re.sub(r"(^\")", r'\1 ', text)
    text = re.sub(r"(^\')", r'\1 ', text)
    text = re.sub(r"('\'$)", r' \1', text)
    text = re.sub(r"('\"$)", r' \1', text)

    #Separate parentheses where appropriate
    text = re.sub(r"(\)\s)", r' \1', text)
    text = re.sub(r"(\s\()", r'\1 ', text)

    # Separate periods that come before newline or end of string.
    text = re.sub('\. *(\n|$)', ' . ', text)
    
    # separate single quotes in the middle of words
    # text = re.sub(r"(\w)(\')(\w)", r'\1 \2 \3', text)
    
    # separate out 's at the end of words
    text = re.sub(r"(\w)(\'s)(\s)", r"\1 s ", text)
    split_text = text.split()
    
    if stem_text:
        result = [stemmer.stem(w) for w in split_text]
        split_text = result

    if alpha_only:
        split_text = return_alpha_only(split_text)
    return split_text
