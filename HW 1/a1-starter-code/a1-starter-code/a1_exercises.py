def is_a_triple(n):
    """Return True if n is a multiple of 3; False otherwise."""

    if n % 3 == 0:
        return True
    else: 
        return False
    
def last_prime(m):
    """Return the largest prime number p that is less than or equal to m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    
    def is_prime(n):
        if n <= 1:
            return False
        else:
            for i in range(2, n):
                if (n % i) == 0:
                    return False
            else:
                return True

    if m < 2: 
        return None
    for i in range(m, 1, -1):
        if is_prime(i):
            return i

def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""

    if b**2 - 4*a*c < 0:
        return 'complex'

    elif b**2 - 4*a*c == 0:
        return -b / (2*a)
    
    else:
        r1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
        r2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)
        return (r1, r2)
    
def new_quadratic_function(a, b, c):
    """Create and return a new, anonymous function (for example
    using a lambda expression) that takes one argument x and 
    returns the value of ax^2 + bx + c."""

    return lambda x: a*x**2 + b*x + c


def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    Perfect shuffle means splitting a list into two halves and then interleaving
    them. For example, the perfect shuffle of [0, 1, 2, 3, 4, 5, 6, 7] is
    [0, 4, 1, 5, 2, 6, 3, 7]."""

    half1 = even_list[:len(even_list)//2]
    half2 = even_list[len(even_list)//2:]

    list = []

    for i in range(len(even_list)//2):
        list.append(half1[i])
        list.append(half2[i])
    return list


def list_of_3_times_elts_plus_1(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 3 and had 1 added to it."""

    return [(i * 3 + 1) for i in input_list]
    

def triple_vowels(text):
    """Return a new version of text, with all the vowels tripled.
    For example:  "The *BIG BAD* wolf!" => "Theee "BIIIG BAAAD* wooolf!".
    For this exercise assume the vowels are
    the characters A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""

    vowels = "aeiouAEIOU"
    new_text = []

    for i in text:
        if i in vowels:
            new_text.append(i*3)
        else:
            new_text.append(i)
    return ''.join(new_text)

import re

def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', *', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ] { } | : ).
    Convert all the letters to lower-case before the counting."""

    def is_char(char):
        valid_char = "abcdefghijklmnopqrstuvwxyz0123456789-+*/@#%'"
        return char in valid_char
    lowertext = text.lower()
    word = ''
    count = {}
    for char in lowertext:
        if is_char(char):
            word += char
        else:
            if word:
                count[word] = count.get(word, 0) + 1
                word = ''
    if word:
        count[word] = count.get(word, 0) + 1
    return count
