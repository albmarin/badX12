from badx12 import Parser

parser = Parser()

with open(r'C:\Users\e149087\Documents\Data Lake Project\small_sample.edi', 'r', encoding='utf-8-sig') as f:
    document = parser.parse_document(f.read())

    print(document.interchange.txi)
