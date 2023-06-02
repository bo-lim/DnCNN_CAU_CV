import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
import time
from torch.utils.data import DataLoader
from models import DnCNN
from utils import MSE_loss, get_lr_scheduler




# from dataloader_utils import train, train_dataloader, test_dataloader
def train_dataloader(train_dataset):
    train_dataloader = DataLoader(
        dataset=train_dataset,
        batch_size=64,
        num_workers=2,
        persistent_workers=True,
        sampler=torch.utils.data.RandomSampler(train_dataset),
    )
    return train_dataloader

def test_dataloader(test_dataset):
    test_dataloader = DataLoader(
        dataset=test_dataset,
        batch_size=1,
        num_workers=1,
        persistent_workers=True,
        drop_last=False,
        sampler=torch.utils.data.SequentialSampler(test_dataset),
    )
    return test_dataloader

def train(opt):
    # Config 파일에서 가져오기
    lr = 0.01
    n_epoch = 500
    batch_size = 64
    PATH = './models/'
    lr_scheduler_name = 'MultiStepLR'

    # Define dataset_type based on the configuration
    dataset_type = opt['datasets']['train']['dataset_type']

    # Iterate over phases (train, test)
    for phase, dataset_opt in opt['datasets'].items():
        if phase == 'train':
            train_dataset = define_Dataset(dataset_opt)
            train_dataloader = train_dataloader(train_dataset)
        elif phase == 'test':
            avg_psnr = 0.0
            test_dataset = define_Dataset(dataset_opt)
            test_dataloader = test_dataloader(test_dataset)
        else:
            raise NotImplementedError("Phase [%s] is not recognized." % phase)

        if phase == 'train':
            model = DnCNN()
            model.cuda()
            model.train()
            criterion = MSE_loss()
            optimizer = optim.Adam(model.parameters(), lr=lr)
            lr_scheduler = get_lr_scheduler(lr_scheduler_name, optimizer=optimizer)
            for epoch in range(0, n_epoch):
                epoch_loss = 0
                st = time.time()
                for xy in train_dataloader:
                    x, y = xy[0].cuda(), xy[1].cuda() # x: noisy image, y:ground truth
                    optimizer.zero_grad()
                    prediction = model(x)
                    loss = criterion(prediction, y)
                    epoch_loss = loss.item()
                    loss.backward()
                    optimizer.step()
                et = time.time() - st
                lr_scheduler.step()
                print(f'epoch : {epoch}, loss : {epoch_loss/batch_size}, time : {et}')

            torch.save(model, PATH+'DnCNN.pth')
        elif phase == 'test':
            pass


    val_dataloader = test_dataloader
