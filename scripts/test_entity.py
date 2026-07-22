from parser.pdf_parser import PDFParser
from models.factory import create_model
from omegaconf import OmegaConf
from prompts.entity_prompt import ENTITY_PROMPT

cfg = OmegaConf.load("configs/config.yaml")
model = create_model(cfg)
parser = PDFParser("data/raw/sample.pdf")
doc = parser.parse()
page = doc.pages[0]
response = model.generate(
    image=page.image_path,
    text=page.text,
    prompt=ENTITY_PROMPT,
)

print(response.text)