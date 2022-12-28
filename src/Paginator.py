from typing import List, Tuple
from src.Concordance import Entry

def splitEntry(entry: Entry, at: int) -> Tuple[Entry, Entry]:
    
    base_split = entry['split_num'] if entry['split_num'] != -1 else 0
    
    return (
        Entry(word = entry['word'], 
              total = entry['total'], 
              occurrences = entry['occurrences'][:at], 
              split_num = base_split
        ),
        Entry(word = entry['word'], 
              total = entry['total'],
              occurrences = entry['occurrences'][at:],
              split_num = base_split+1
        ))

class Page():
    
    def __init__(self, size: int):
        self.entry_list: List[Entry] = []
        self.new_words: List[str] = []
        self.open = size
        
    def __add_entry(self, entry: Entry):
        self.entry_list.append(entry)
        self.open -= len(entry['occurrences'])
        if entry['split_num'] <= 0:
            self.new_words.append(entry['word'])
        
    def add_entry(self, entry: Entry) -> Entry:
        if len(entry['occurrences']) <= self.open:
            self.__add_entry(entry)
            return None
        else:
            entry1, entry2 = splitEntry(entry, self.open)
            self.__add_entry(entry1)
            return entry2

def Paginate(entries: List[Entry], page_size: int):
    
    pagelist: List[Page] = [Page(page_size)]
    
    def add_entry_pagelist(entry: Entry):
        if not pagelist[-1].open:
            pagelist.append(Page(page_size))
        return pagelist[-1].add_entry(entry)
    
    for entry in entries:
        ret = add_entry_pagelist(entry)
        while ret:
            ret = add_entry_pagelist(ret)
            
    return pagelist