from pathlib import Path
from omegaconf import OmegaConf

class Config:
    def __init__(self,
                 config_path="configs/config.yaml"):
        self.cfg = OmegaConf.load(config_path)

    @property
    def project(self):
        return self.cfg.project

    @property
    def parser(self):
        return self.cfg.parser

    @property
    def llm(self):
        return self.cfg.llm

    @property
    def embedding(self):
        return self.cfg.embedding

    @property
    def retrieval(self):
        return self.cfg.retrieval