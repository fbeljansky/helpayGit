import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

class BilleteClassifierPesos(nn.Module):
    def __init__(self, num_classes=32):
        super(BilleteClassifierPesos, self).__init__()
        self.resnet = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.resnet(x)
