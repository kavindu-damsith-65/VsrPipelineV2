import torch
import torch.nn.functional as F

class DummyForkNet(torch.nn.Module):
    def forward(self, x):
        return F.interpolate(x, scale_factor=4, mode="bilinear")

class ModelManager:
    def __init__(self, device="cuda"):
        self.device = device
        self.models = {
            "ForkNet": DummyForkNet().to(device).eval(),
            "Bicubic": None
        }
        self.active = "ForkNet"

    def set(self, name):
        self.active = name

    def run(self, x):
        if self.active == "Bicubic":
            return F.interpolate(x, scale_factor=4, mode="bicubic")
        with torch.no_grad():
            return self.models[self.active](x)
