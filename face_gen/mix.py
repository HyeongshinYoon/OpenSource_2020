import math

import torch
from torchvision import utils

from face_gen.model import StyledGenerator
from face_gen.mean_style import get_mean_style


@torch.no_grad()
def style_mixing(source, target):

    source_code = torch.tensor(source)
    target_code = torch.tensor(target)

    # If you have a GPU, change device to cuda
    device = 'cpu'
    alpha = 1
    step = int(math.log(256, 2)) - 2

    generator = StyledGenerator(512).to(device)
    generator.load_state_dict(torch.load(
        "./checkpoint/stylegan-256px-new.model", map_location=torch.device(device))['g_running'])
    generator.eval()

    mean_style = get_mean_style(generator, device)

    image = generator(
        [target_code[0].unsqueeze(0).repeat(1, 1), source_code],
        step=step,
        alpha=alpha,
        mean_style=mean_style,
        style_weight=0.7,
        mixing_range=(0, 1),
    )

    img_grid = utils.make_grid(
        image, nrow=1, normalize=True, range=(-1, 1)
    )

    return img_grid
