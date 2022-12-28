from typing import List, TypedDict

class Occurence(TypedDict):
    location: str
    line_text: str

def init_occurence(book: int, canto: str, stanza: int, 
                line_num: int, whole_line: str):
    location = (f'Book {book}, {canto}, '
                f'{stanza}.{line_num}')
    return Occurence(location = location, line_text = whole_line)

def show_occurence(occurence: Occurence):
    return (f'{occurence["location"]}: "{occurence["line_text"]}";\n')


class Entry(TypedDict):
    word: str
    total: int
    occureneces: List[Occurence]

class Concordance:
    def __init__(self):
        self.data = {}
    
    def add_word(self, book: int, canto: str, stanza: int, 
                 line_num: int, whole_line: str, word: str):
        occurence = init_occurence(book, canto, stanza, line_num, whole_line)
        if word in self.data:
            self.data[word].append(occurence)
        else:
            self.data[word] = [occurence]
    
    def show(self):
        ret = ""
        for word in sorted(self.data.keys()):
            ret += f'"{word.title()}": {len(self.data[word])} total;\n'
            for occurence in self.data[word]:
                ret += '\t' + show_occurence(occurence)
        return ret
    
    def toEntryList(self) -> List[Entry]:
        return [Entry(word = word, 
                      total = len(self.data[word]),
                      occurences = self.data[word])
                for word in sorted(self.data.keys())]
            

