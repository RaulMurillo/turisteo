#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import string


def del_sqrBrackets(text):
    """Removes the square brackets (and their content) from text.

    :param str text: The text to be cleaned of [ ].  
    :return: Same text without square brackets.  
    """
    regex = re.compile(r'\s?[\[].*?[\]]')
    result = re.sub(regex, '', text)
    return result


def del_refs(text):
    """ Removes the references (in square brackets) from text.

    :param str text: The text to be cleaned of references.  
    :return: Same text without references.  
    """
    regex_num = re.compile(r'\s?[\[][0-9]+[\]]')
    regex_text = re.compile(r'\s?[\[][\w ]*needed[\w ]*[\]]')
    result = re.sub(regex_num, '', text)
    result = re.sub(regex_text, '', result)
    return result


def find_nonAscii(text):
    """ Return the first appearance of a non-ASCII character (in a `Match` object), or `None`. """
    regex = re.compile(r'([^\x00-\x7F])+')
    return re.search(regex, text)


def check_parentheses(s):
    """ Return True if the parentheses in string s match, otherwise False. """
    j = 0
    for c in s:
        if c == ')':
            j -= 1
            if j < 0:
                return False
        elif c == '(':
            j += 1
    return j == 0


def find_parentheses(s):
    """ Find and return the location of the matching parentheses pairs in s.

    Given a string, s, return a dictionary of start: end pairs giving the
    indexes of the matching parentheses in s. Suitable exceptions are
    raised if s contains unbalanced parentheses.

    """
    # The indexes of the open parentheses are stored in a stack, implemented
    # as a list

    stack = []
    parentheses_locs = {}
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            try:
                parentheses_locs[stack.pop()] = i
            except IndexError:
                raise IndexError('Too many close parentheses at index {}'
                                 .format(i))
    if stack:
        raise IndexError('No matching close parenthesis to open parenthesis '
                         'at index {}'.format(stack.pop()))
    return parentheses_locs


def del_nonAscii(text):
    # match = find_nonAscii(text)
    # if match!=None:
    if check_parentheses(text):
        parentheses_locs = find_parentheses(text)
        parentheses_locs = sorted(
            [(k, v) for k, v in parentheses_locs.items()])
        # Remove nested parenthesis
        i = 1
        while i < len(parentheses_locs):
            if parentheses_locs[i][0] < parentheses_locs[i-1][1]:
                parentheses_locs.pop(i)
            else:
                i += 1
        # Remove non-ASCII characters
        parentheses_locs.reverse()
        for k, v in parentheses_locs:
            s0 = text[:k-1]
            s1 = text[k-1:v+1]
            s2 = text[v+1:]
            if find_nonAscii(s1):
                text = s0 + s2
    return text

def del_coordinates(text):
    regex = re.compile(r'Coordinates:\s?[^\n]*\n')
    result = re.sub(regex, '', text)
    return result


if __name__ == "__main__":
    x = "The Taj Mahal (/ˌtɑːdʒ məˈhɑːl, ˌtɑːʒ-/;[4] lit. Crown of the Palace, [taːdʒ ˈmɛːɦ(ə)l])[5] is an ivory-white marble mausoleum on the south bank of the Yamuna river in the Indian city of Agra. It was commissioned in 1632 by the Mughal emperor Shah Jahan (reigned from 1628 to 1658) to house the tomb of his favourite wife, Mumtaz Mahal; it also houses the tomb of Shah Jahan himself. The tomb is the centrepiece of a 17-hectare (42-acre) complex, which includes a mosque and a guest house, and is set in formal gardens bounded on three sides by a crenellated wall."
    y = del_nonAscii(del_refs(x))
    print(y)
