import torch
import numpy as np

class Pipeline:
    def __init__(self, model):
        self.model = model

    def process(self, frame):
        # numpy → torch
        x = torch.from_numpy(frame).permute(2,0,1).unsqueeze(0)
        x = x.float().cuda() / 255.0

        # SR
        y = self.model.run(x)

        # torch → numpy
        y = (y.clamp(0,1) * 255).byte()
        y = y.squeeze(0).permute(1,2,0).cpu().numpy()
        return y
