import math

import torch
from torchvision import utils
from face_gen.mean_style import get_mean_style

from face_gen.model import StyledGenerator

@torch.no_grad()
def face_gen():
    device = 'cuda'
    style = torch.randn(1, 512).to(device)
    step = int(math.log(256, 2)) - 2

    generator = StyledGenerator(512).to(device)
    generator.load_state_dict(torch.load("\checkpoint\stylegan-256px-new.model")['g_running'])
    generator.eval()

    mean_style = get_mean_style(generator, device)

    image = generator(
        style,
        step=step,
        alpha=1,
        mean_style=mean_style,
        style_weight=0.7,
    )

    utils.save_image(
        image, f'{img_name}.png', nrow=1, normalize=True, range=(-1, 1)
    )

    return style
