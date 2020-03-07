import re


def del_sqrBrackets(text):
    # regex = re.compile('[\(\[].*?[\)\]]')
    # regex = re.compile('[ ]?[\(].*?[\)]')
    regex = re.compile('\s?[\[].*?[\]]')
    result = re.sub(regex, '', text)
    return result


if __name__ == "__main__":
    x = "This is a sentence. (once a day) [twice a day]"
    y = del_sqrBrackets(x)
    print(y)
