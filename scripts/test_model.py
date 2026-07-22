from omegaconf import OmegaConf
from models.factory import create_model

cfg = OmegaConf.load("configs/config.yaml")
model = create_model(cfg)
print("Everything OK!")