import os
import nltk
import re
from xml.etree import ElementTree
from utilities import load_entire_directory
import numpy as np
import pylab
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

def norm_vec(vec):
    mag = np.dot(vec, vec)
    if mag == 0:
        return vec
    else:
        return(vec / (np.sqrt(mag)))

    
def load_seasons_corpus():
    raw_corpus_files = load_entire_directory('corpora/seasons')
    corpus_dict = {}
    for fname in raw_corpus_files.keys():
        raw_file = raw_corpus_files[fname]
        new_etree = ElementTree.XML(raw_file)
        entry_text = new_etree.find("BODY/SEASONS").text
        student_name = new_etree.find("PNAME").text
        human_code = new_etree.find("TCODE").text
        separated_text = separate_turns(entry_text)
        student_text = ""
        for turn in separated_text:
            if turn[0] == student_name:
                student_text += turn[1] + "\n"
        short_name = re.sub(r"\.xml", "", fname)
        corpus_dict[short_name] = [seasons_tokenize(student_text), human_code]
    return corpus_dict


def load_seasons_corpus_as_utterances():
    raw_corpus_files = load_entire_directory('corpora/seasons')
    corpus_dict = {}
    for fname in raw_corpus_files.keys():
        raw_file = raw_corpus_files[fname]
        new_etree = ElementTree.XML(raw_file)
        entry_text = new_etree.find("BODY/SEASONS").text
        student_name = new_etree.find("PNAME").text
        human_code = new_etree.find("TCODE").text
        separated_text = separate_turns(entry_text)
        student_text_list = []
        for turn in separated_text:
            if turn[0] == student_name:
                student_text_list.append(turn[1])
        short_name = re.sub(r"\.xml", "", fname)
        tokenzed_utterances = [seasons_tokenize(utterance) for utterance in student_text_list]
        corpus_dict[short_name] = [tokenzed_utterances, human_code]
    return corpus_dict


def load_seasons_corpus_no_tokenize():
    raw_corpus_files = load_entire_directory('corpora/seasons')
    corpus_dict = {}
    for fname in raw_corpus_files.keys():
        raw_file = raw_corpus_files[fname]
        new_etree = ElementTree.XML(raw_file)
        entry_text = new_etree.find("BODY/SEASONS").text
        student_name = new_etree.find("PNAME").text
        human_code = new_etree.find("TCODE").text
        separated_text = separate_turns(entry_text)
        student_text = ""
        for turn in separated_text:
            if turn[0] == student_name:
                student_text += turn[1] + "\n"
        short_name = re.sub(r"\.xml", "", fname)
        corpus_dict[short_name] = [student_text, human_code]
    return corpus_dict


def max_from_dict(the_dict):
    key, value = max(the_dict.iteritems(), key=lambda x:x[1])
    return key


def weight_factor(tf, df, cf, N):
    if tf == 0:
        result = 0
    else:
        result = (1 + np.log(tf)) * np.log(N  / df)
    return result


def weight_factor2(tf, df, cf, N):
    if tf == 0:
        result = 0
    else:
        result = (1 + np.log(tf))
    return result


def load_seasons_comparison_files():
    raw_comparison_files = load_entire_directory('corpora/seasonscomparisondocs')
    comparison_dict = {}
    for fname in raw_comparison_files.keys():
        short_name = re.sub(r"\.txt", "", fname)
        comparison_dict[short_name] = seasons_tokenize(raw_comparison_files[fname])
    return comparison_dict


def separate_turns(raw_text):
    return re.findall(r"(\w+?)\t(.*?)\n", raw_text)


def orthogonalize(doc_vectors):
        total_v = np.zeros(len(doc_vectors[doc_vectors.keys()[0]]))
        for name in doc_vectors.keys():
                total_v = total_v + doc_vectors[name]
        total_v = norm_vec(total_v)
        new_doc_vectors = {}
        for name in doc_vectors.keys():
            v = doc_vectors[name]
            new_doc_vectors[name] = norm_vec(v - np.dot(v, total_v) * total_v)
        return new_doc_vectors


def bar_chart(resultlist, code_names):
    ldata = {}
    i = 0
    for code in code_names:
        ldata[code] = [r[code] for r in resultlist]
    ind = pylab.arange(len(resultlist))
    width = 1.0 / (len(code_names) + 1)
    lcolors = ['red', 'green', 'blue']
    
    for c in range(len(code_names)):
        pylab.bar(ind + c * width, ldata[code_names[c]], width, color=lcolors[c])
        # bar_groups.append(bars)

    pylab.xticks(pylab.arange(len(resultlist)))
    pylab.xlim(xmax=len(resultlist))
    pylab.grid(True)
    pylab.show()

    
def normalize_columns(mat):
    mat_norm = np.copy(mat)
    for i in range(mat.shape[1]):
        mat_norm[:, i] = norm_vec(mat[:, i])
    return mat_norm


contraction_patterns = re.compile(r"(?i)(.)('ll|'re|'ve|n't|'s|'m|'d)\b")
def is_contraction(the_text):
        return contraction_patterns.search(the_text)

    
def alpha_only (ltext):
    return [w.lower() for w in ltext if (len(w) > 0) and (w.isalpha() or w[0]=='<' or is_contraction(w))]


def seasons_tokenize(text, stem_text = False):
    # Separate most punctuation
    text = re.sub(r"(\w)([\.\-\/&\";:\(\)\?\!\]\[\{\}\*])", r'\1 \2 ', text)

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

    # Separate leading .'s and leading ['s]
    text = re.sub(r"(\.)(\w)", r'\1 \2', text)
    text = re.sub(r"(\[)(\w)", r'\1 \2', text)
    
    # remove forward slashes
    text = re.sub(r"/", "", text)

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
    split_text = alpha_only(split_text)
    if stem_text:
        result = [stemmer.stem(w) for w in split_text]
        split_text = result

    return split_text