#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:56:49 2017

@author: jojo
"""
import string
import porter2_jojo
import re

#processing email.
#start by counting characters.
SU = string.ascii_uppercase
SL = string.ascii_lowercase
No = string.digits
def get_char_counts(string):
    """
    counts the type of characters in each string, 
    perhaps this could encode some useful features. 
    perhaps not!
    """
    char_count = [0, 0, 0, 0]
    for char in string:
        if char in SU:
            char_count[0] = char_count[0]+1
        elif char in SL:
            char_count[1] = char_count[1] +1
        elif char in No:
            char_count[2] = char_count[2]+1
        else:
            #assumes all other characters are special :-)
            char_count[3] = char_count[3] +1

    return char_count

#print (get_char_counts('string'))


def get_word_counts(line, minimalStemming=False, stopWordsRemoved=True, ):
    """
    constructs bag of words as dictionary
    """
    word_count = {}
    line = re.sub('[^a-zA-Z]+', ' ', line)
    words = line.split()
    for word in words:
        
        word = porter2_jojo.stem(word, minimalStemming, stopWordsRemoved)
        if word:
            try:
                word_count[word] = word_count[word] + 1
            except:
                word_count[word] =1
    return word_count


#print (get_char_counts('You are receiving this letter because you have expressed an interest in '))
#print(get_word_counts('You are receiving this letter because you have expressed an interest in '))
