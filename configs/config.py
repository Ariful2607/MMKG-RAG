from pathlib import Path
from omegaconf import OmegaConf


def load_config(config_file="config.yaml"):

    config_path = Path(__file__).parent / config_file

    cfg = OmegaConf.load(config_path)

    return cfg