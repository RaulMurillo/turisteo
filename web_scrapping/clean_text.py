# -*- coding: utf-8 -*-
import re


def del_sqrBrackets(text):
    """Removes the square brackets (and their content) from text.

    :param str text: The text to ble cleaned of [ ].  
    :return: Same text without square brackets.  
    """

    # regex = re.compile(r'[\(\[].*?[\)\]]')
    # regex = re.compile(r'[ ]?[\(].*?[\)]')
    regex = re.compile(r'\s?[\[].*?[\]]')
    result = re.sub(regex, '', text)
    return result


if __name__ == "__main__":
    x = "This is a sentence. (once a day) [twice a day]"
    y = del_sqrBrackets(x)
    print(y)
