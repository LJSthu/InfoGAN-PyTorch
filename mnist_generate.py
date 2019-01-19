import argparse

import torch
import torchvision.utils as vutils
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-load_path', required=True, help='Checkpoint to load path from')
args = parser.parse_args()

import sys
sys.path.append('/home/mohit/DeepLearning/InfoGAN/')
from models.mnist_model import Generator

# Load the checkpoint file
state_dict = torch.load(args.load_path)

# Set the device to run on: GPU or CPU.
device = torch.device("cuda:0" if(torch.cuda.is_available()) else "cpu")
# Get the 'params' dictionary from the loaded state_dict.
params = state_dict['params']

# Create the generator network.
netG = Generator().to(device)
# Load the trained generator weights.
netG.load_state_dict(state_dict['netG'])
print(netG)

c = np.linspace(-1, 1, 10).reshape(1, -1)
c = np.repeat(c, 10, 0).reshape(-1, 1)
c = torch.from_numpy(c).float().to(device)
c = c.view(100, 1, 1, 1)

zeros = torch.zeros(100, 1, 1, 1, device=device)

c2 = torch.cat((c, zeros), dim=1)
c3 = torch.cat((zeros, c), dim=1)

idx = np.arange(10).repeat(10)
dis_c = torch.zeros(100, 10, 1, 1, device=device)
dis_c[torch.arange(0, 100), idx] = 1.0

c1 = dis_c.view(100, -1, 1, 1)

z = torch.randn(100, 62, 1, 1, device=device)

noise1 = torch.cat((z, c1, c2), dim=1)
noise2 = torch.cat((z, c1, c3), dim=1)

with torch.no_grad():
    generated_img1 = netG(noise1).detach().cpu()
# Display the generated image.
plt.axis("off")
plt.title("Generated Images Variation in c2")
plt.imshow(np.transpose(vutils.make_grid(generated_img1, nrow=10, padding=2, normalize=True), (1,2,0)))

with torch.no_grad():
    generated_img2 = netG(noise2).detach().cpu()
# Display the generated image.
plt.axis("off")
plt.title("Generated Images Variation in c3")
plt.imshow(np.transpose(vutils.make_grid(generated_img2, nrow=10, padding=2, normalize=True), (1,2,0)))
plt.show()