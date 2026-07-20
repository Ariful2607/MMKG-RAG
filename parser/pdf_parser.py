from pathlib import Path
import fitz
from parser.page import Page
from parser.document import Document


class PDFParser:

    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(pdf_path)

    @property
    def num_pages(self):
        return len(self.doc)

    def extract_text(self, page_index):
        page = self.doc.load_page(page_index)
        return page.get_text()

    def render_page(self, page_index, output_dir):
        page = self.doc.load_page(page_index)

        pix = page.get_pixmap(dpi=200)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        image_path = output_dir / f"page_{page_index+1}.png"

        pix.save(image_path)

        return image_path

    # def parse(self, output_dir="data/processed/pages"):
    #     pages = []

    #     for idx in range(self.num_pages):
    #         text = self.extract_text(idx)
    #         image = self.render_page(idx, output_dir)

    #         pages.append(
    #             Page(
    #                 page_number=idx + 1,
    #                 text=text,
    #                 image_path=image,
    #             )
    #         )
    #     return pages

    def parse(self, output_dir="data/processed/pages"):
        document = Document(
            name=self.pdf_path.stem,
            path=self.pdf_path,
        )

        for idx in range(self.num_pages):

            text = self.extract_text(idx)
            image = self.render_page(idx, output_dir)

            document.add_page(
                Page(
                    page_number=idx + 1,
                    text=text,
                    image_path=image,
                )
            )

        return document