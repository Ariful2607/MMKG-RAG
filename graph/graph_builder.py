class GraphBuilder:
    def __init__(
        self,
        extractor,
        graph,
    ):
        self.extractor = extractor
        self.graph = graph

    def process_page(self, page):
        entities = self.extractor.extract(page)
        for entity in entities:
            self.graph.add_entity(entity)

    def process_document(self, document):
        for page in document.pages:
            self.process_page(page)