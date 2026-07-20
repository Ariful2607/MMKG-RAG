from parser.pdf_parser import PDFParser

parser = PDFParser("data/raw/sample.pdf")

document = parser.parse()

print(document.name)
print(document.num_pages)
print(document.pages[0])