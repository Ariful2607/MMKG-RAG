import torch

def get_device():
    if torch.cuda.is_available():
        return "cuda"

    if torch.backends.mps.is_available():
        return "mps"

    return "cpu"


def get_dtype(device):
    if device == "cuda":
        return torch.bfloat16

    if device == "mps":
        return torch.float16

    return torch.float32