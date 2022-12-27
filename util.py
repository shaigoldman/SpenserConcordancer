from typing import List

def filter_valid_str(slist: List[str]):
    return [s for s in slist if s != '']

def filter_valid_o(olist: List):
    return [obj for obj in olist if obj.valid]

def filter_alpha(word: str):
    return ''.join([c for c in word if c.isalpha() or c == '&'])

def fix_th_prefix(word: str):
    if 'th\'' not in word:
        return [word]
    return ['the', word.split('\'')[1]]

def concat(lists: List[List]):
    x = []
    for list in lists:
        x.extend(list)
    return x