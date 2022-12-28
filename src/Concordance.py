from typing import List, TypedDict

class Occurrence(TypedDict):
    location: str
    line_text: str

def init_occurrence(book: int, canto: str, stanza: int, 
                line_num: int, whole_line: str):
    location = (f'Book {book}, {canto}, '
                f'{stanza}.{line_num}')
    return Occurrence(location = location, line_text = whole_line)

def show_occurrence(occurrence: Occurrence):
    return (f'{occurrence["location"]}: "{occurrence["line_text"]}";\n')

class Entry(TypedDict):
    word: str
    total: int
    occureneces: List[Occurrence]
    split_num: int # will be important for paginator.py

class Concordance:
    def __init__(self):
        self.data = {}
    
    def add_word(self, book: int, canto: str, stanza: int, 
                 line_num: int, whole_line: str, word: str):
        occurrence = init_occurrence(book, canto, stanza, line_num, whole_line)
        if word in self.data:
            self.data[word].append(occurrence)
        else:
            self.data[word] = [occurrence]
    
    def show(self):
        ret = ""
        for word in sorted(self.data.keys()):
            ret += f'"{word.title()}": {len(self.data[word])} total;\n'
            for occurrence in self.data[word]:
                ret += '\t' + show_occurrence(occurrence)
        return ret
    
    def toEntryList(self) -> List[Entry]:
        return [Entry(word = word, 
                      total = len(self.data[word]),
                      occurrences = self.data[word],
                      split_num=-1)
                for word in sorted(self.data.keys())]
            

