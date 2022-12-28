class ConcordanceEntry:
    def __init__(self, book: int, canto: str, stanza: int, 
                line_num: int, whole_line: str):
        self.book = book
        self.canto = canto
        self.stanza = stanza
        self.line_num = line_num
        self.whole_line = whole_line
    
    def location(self):
        return (f'Book {self.book}, {self.canto}, '
                f'{self.stanza}.{self.line_num}')
    
    def show(self):
        return (f'{self.location()}: "{self.whole_line}";\n')
    
    def toJSON(self):
        return {"location": self.location(), "whole_line": self.whole_line}

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
            ret += f'"{word.title()}": {len(self.data[word])} total;\n'
            for entry in self.data[word]:
                ret += '\t' + entry.show()
        return ret
    
    def toJSON(self):
        return [{"word": word, 
                 "total": len(occurences),
                 "occurences": occurences}
                for word in sorted(self.data.keys())
                if (occurences := [entry.toJSON() for entry in self.data[word]])]
            

