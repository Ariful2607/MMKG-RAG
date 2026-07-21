from parser.pdf_parser import PDFParser
from models.ollama_llm import OllamaLLM
from extraction.entity_extractor import EntityExtractor

parser = PDFParser("data/raw/sample.pdf")
document = parser.parse()

llm = OllamaLLM(
    "qwen2.5:7b"
)

extractor = EntityExtractor(llm)

entities = extractor.extract(
    document.pages[0]
)

for e in entities:
    print(e)