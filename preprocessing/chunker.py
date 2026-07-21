class TextChunker:
    def __init__(
        self,
        chunk_size=300,
        overlap=50,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text):
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunks.append(
                " ".join(words[start:end])
            )
            start += self.chunk_size - self.overlap
        return chunks