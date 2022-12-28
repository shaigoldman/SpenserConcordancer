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
    pages_paths = ['ret/concordance', 
                   '../spenser-concordance-app/src/resources/concordance'
                   ]
    pagelist = Paginate(entrylist, PAGE_SIZE)
    for i, page in enumerate(pagelist):
        for path in pages_paths:
            fname = f'{path}/page{i}.json'
            print(f'Wrote page {i} text to {fname}')
            with open(fname, 'w') as f:
                json.dump(page.entry_list, f)
        
    print(f'Wrote concordance json to {concordance_fname}')

if __name__ == "__main__":
    main()