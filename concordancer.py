from typing import List

argument_id = 'argument'

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


class ConcordanceEntry:
    def __init__(self, book: int, canto: str, stanza: int, 
                line_num: int, whole_line: str):
        self.book = book
        self.canto = canto
        self.stanza = stanza
        self.line_num = line_num
        self.whole_line = whole_line
    
    def show(self):
        return (f'Book {self.book}, {self.canto}, '
                f'{self.stanza}.{self.line_num}: "{self.whole_line}".\n')

class Concordance:
    def __init__(self):
        self.data = {}
    
    def add_word(self, book: int, canto: str, stanza: int, 
                 line_num: int, whole_line: str, word: str):
        entry = ConcordanceEntry(book, canto, stanza, line_num, whole_line)
        if word in self.data:
            self.data[word].append(entry)
        else:
            self.data[word] = [entry]
    
    def show(self):
        ret = ""
        for word in sorted(self.data.keys()):
            ret += f'"{word.title()}": {len(self.data[word])} total occurances.\n'
            for entry in self.data[word]:
                ret += '\t' + entry.show()
        return ret
            

class Line:
    def __init__(self, book: int, canto: str, stanza: int, 
                 id: int, raw: str, fix_first=False):
        self.book = book
        self.canto = canto
        self.stanza = stanza
        self.id = id
        self.line = raw.strip()
        self.valid = self.line != ''
        if fix_first:
            self.fix_first_word()
        words = concat([fix_th_prefix(w.lower()) for w in filter_valid_str(self.line.split(' '))])
        self.words = filter_valid_str([filter_alpha(w) for w in words])
    
    # the first word of a stanza can have a bug where the first letter is cut off
    def fix_first_word(self):
        line_words = self.line.split(' ')
        first_word = line_words[0]
        second_word = line_words[1]
        if (first_word == "O" or first_word == "A") and len(second_word)>1:
            return
        if first_word == "VV":
            first_word = "W"
        if len(first_word) > 1:
            self.line = ' '.join([first_word.title()] + line_words[1:])
        elif second_word != '' and second_word[0].isupper():
            joinedword = ''.join([first_word, second_word]).title()
            self.line = ' '.join([joinedword] + line_words[2:])
    
    def concord_line(self, ccd: Concordance):
        for word in self.words:
            ccd.add_word(self.book, self.canto, self.stanza, self.id, self.line, word)
    
    def print_line(self):
        print(f'   {self.id}: {self.line} | {self.words}')


class Stanza:
    def __init__(self, book: int, canto: str,
                 id: int, raw: str):
        self.book = book
        self.canto = canto
        self.id = id
        self.lines = filter_valid_o(
            [Line(self.book, self.canto, self.id, i+1, txt, self.id == 1)
             for i, txt in enumerate(filter_valid_str(raw.split('\n')))])
    
    def concord_stanza(self, ccd: Concordance):
        for line in self.lines:
            line.concord_line(ccd)
            
    def print_stanza(self):
        if self.id == argument_id:
            print(f'Argument: ')
        else:
            print(f'  Stanza {self.id}')
        [line.print_line() for line in self.lines]
        print()
   

class Canto:
    def __init__(self, book: int, id: str, argument: str, stanzas: str):
        self.book = book
        self.id = id.strip()
        self.argument = Stanza(self.book, self.id, argument_id, argument)
        self.stanzas = [Stanza(self.book, self.id, i+1, s)
                        for i, s in enumerate(filter_valid_str(stanzas.split('\n\n')))]
    
    def concord_canto(self, ccd: Concordance):
        self.argument.concord_stanza(ccd)
        for stanza in self.stanzas:
            stanza.concord_stanza(ccd)
        
    def print_canto(self):
        print(f"ID: {self.id}")
        self.argument.printStanza()
        print("Stanzas:")
        [s.print_stanza() for s in self.stanzas]
        
class Book:
    splitter = '_' * 66
    
    def __init__(self, id: int, raw: str):
        self.id = id
        self.cantos = self.read_book(raw)
        
    def read_book(self, text):
        splits = text.split(self.splitter)
        splitsgen = (s for s in splits)
        splitslen = len(splits)
            
        proem = Canto(self.id, "Proem", "", next(splitsgen))
        return [proem] + [
            Canto(self.id, next(splitsgen), next(splitsgen), next(splitsgen)) 
            for _ in range(int(splitslen/3))
        ]
    
    def concord_book(self, ccd: Concordance):
        for canto in self.cantos:
            canto.concord_canto(ccd)
    
    def print_book(self):
        [canto.print_canto() for canto in self.cantos]


def read_book_file(book_num: int):
    fname = f'resources/queene{book_num}.txt'
    with open(fname, "r", encoding='latin-1') as f:
        text = f.read()
    print(f'Loaded {fname}')
    return Book(book_num, text)

def main():
    ccd = Concordance()
    books = [read_book_file(i+1) for i in range(6)]
    for book in books:
        book.concord_book(ccd)
    
    concordance_fname = 'concordance.txt'
    with open(concordance_fname, 'w') as f:
        f.write(ccd.show())
        
    print(f'Wrote concordance to {concordance_fname}')
    

if __name__ == "__main__":
    main()