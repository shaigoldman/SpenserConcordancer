import json
import src.FQParser as FQParser
from src.Concordance import Concordance
from src.Paginator import Paginate

PAGE_SIZE = 500

def main():
    ccd = Concordance()
    books = [FQParser.read_book_file(i+1) for i in range(6)]
    for book in books:
        book.concord_book(ccd)
    
    concordance_fname = 'ret/concordance.txt'
    with open(concordance_fname, 'w') as f:
        f.write(ccd.show())
        
    print(f'Wrote concordance text to {concordance_fname}')
    
    entrylist = ccd.toEntryList()
    pagelist = Paginate(entrylist, PAGE_SIZE)
    
    pages_paths = ['ret/concordance', 
                   '../spenser-concordance-app/src/resources/concordance'
                   ]
    
    index = {}
    
    for i, page in enumerate(pagelist):
        for path in pages_paths:
            fname = f'{path}/page{i}.json'
            print(f'Wrote to {fname}')
            with open(fname, 'w') as f:
                json.dump(page.entry_list, f)
        for word in page.new_words:
            index[word] = i
    for path in pages_paths:
        fname = f'{path}/index.json'
        print(f'Wrote to {fname}')
        with open(fname, 'w') as f:
            json.dump(index, f)

if __name__ == "__main__":
    main()