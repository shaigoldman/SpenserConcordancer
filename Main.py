import json
import FQParser
from Concordance import Concordance


def main():
    ccd = Concordance()
    books = [FQParser.read_book_file(i+1) for i in range(6)]
    for book in books:
        book.concord_book(ccd)
    
    concordance_fname = 'concordance.txt'
    with open(concordance_fname, 'w') as f:
        f.write(ccd.show())
        
    print(f'Wrote concordance text to {concordance_fname}')
    
    concordance_fname = 'concordance.json'
    with open(concordance_fname, 'w') as f:
        json.dump(ccd.toJSON(), f)
        
    print(f'Wrote concordance json to {concordance_fname}')

if __name__ == "__main__":
    main()