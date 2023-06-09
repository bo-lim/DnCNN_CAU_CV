import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
from torch.optim.lr_scheduler import *

class MSE_loss(nn.modules.loss._Loss):
    def __init__(self):
        super(MSE_loss, self).__init__()
    def forward(self, y, target):
        return f.mse_loss(y, target)
    
def get_optimizer(optim_name, parameters, lr):
    if optim_name == 'Adam':
        return optim.Adam(parameters, lr)
    elif optim_name == "SGD":
        return optim.SGD(parameters, lr, momentum=0.9)
    else:
        print("Optimizer 이름을 확인해주세요")

def get_lr_scheduler(lr_name, optimizer):
    if lr_name == "MultiStepLR":
        # Config 파일에서 가져오기로 수정(milstones, gamma)
        return MultiStepLR(optimizer, milestones=[200, 350], gamma=0.5)
    elif lr_name == "CosineAnnealingLR":
        # Config 파일에서 가져오기로 수정(T_max, eta_min)
        return CosineAnnealingLR(optimizer, T_max=100, eta_min=0.001)
    else:
        print("learning rate scheduler 이름을 확인해주세요.")
