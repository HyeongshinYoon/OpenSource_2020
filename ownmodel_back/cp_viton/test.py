# coding=utf-8
import torch
import torch.nn as nn
import torch.nn.functional as F

import argparse
import os
import time
from cp_viton.cp_dataset import CPDataset, CPDataLoader
from cp_viton.networks import GMM, UnetGenerator, load_checkpoint

from tensorboardX import SummaryWriter
from cp_viton.visualization import board_add_image, board_add_images, save_images


def get_opt(stage, data_list):
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default=stage)
    parser.add_argument("--gpu_ids", default="")
    parser.add_argument('-j', '--workers', type=int, default=1)
    parser.add_argument('-b', '--batch-size', type=int, default=4)

    parser.add_argument("--dataroot", default="data")
    parser.add_argument("--datamode", default="test")
    parser.add_argument("--stage", default=stage)
    parser.add_argument("--data_list", default=data_list)
    parser.add_argument("--fine_width", type=int, default=384)
    parser.add_argument("--fine_height", type=int, default=512)
    parser.add_argument("--radius", type=int, default=5)
    parser.add_argument("--grid_size", type=int, default=5)
    parser.add_argument('--tensorboard_dir', type=str,
                        default='tensorboard', help='save tensorboard infos')
    parser.add_argument('--result_dir', type=str,
                        default='result', help='save result infos')
    parser.add_argument('--checkpoint', type=str, default=os.path.join(os.getcwd(), 'cp_viton', 'checkpoints'),
                        help='model checkpoint for test')
    parser.add_argument("--display_count", type=int, default=1)
    parser.add_argument("--shuffle", action='store_true',
                        help='shuffle input data')

    opt = parser.parse_args()
    return opt


def test_gmm(opt, test_loader, model, board):
    device = torch.device('cpu')
    model.to(device)
    # model.cuda()
    model.eval()

    base_name = os.path.basename(opt.checkpoint)
    save_dir = os.path.join(os.getcwd(), 'data', 'test')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    warp_cloth_dir = os.path.join(save_dir, 'warp-cloth')
    if not os.path.exists(warp_cloth_dir):
        os.makedirs(warp_cloth_dir)
    warp_mask_dir = os.path.join(save_dir, 'warp-mask')
    if not os.path.exists(warp_mask_dir):
        os.makedirs(warp_mask_dir)

    for step, inputs in enumerate(test_loader.data_loader):
        iter_start_time = time.time()

        c_names = inputs['c_name']
        im = inputs['image'].to(device)
        im_pose = inputs['pose_image'].to(device)
        im_h = inputs['head'].to(device)
        shape = inputs['shape'].to(device)
        agnostic = inputs['agnostic'].to(device)
        c = inputs['cloth'].to(device)
        cm = inputs['cloth_mask'].to(device)
        im_c = inputs['parse_cloth'].to(device)
        im_g = inputs['grid_image'].to(device)

        grid, _ = model(agnostic, c)
        warped_cloth = F.grid_sample(c, grid, padding_mode='border')
        warped_mask = F.grid_sample(cm, grid, padding_mode='zeros')
        warped_grid = F.grid_sample(im_g, grid, padding_mode='zeros')

    save_images(warped_cloth, c_names, warp_cloth_dir)
    save_images(warped_mask*2-1, c_names, warp_mask_dir)


'''
        visuals = [[im_h, shape, im_pose],
                   [c, warped_cloth, im_c],
                   [warped_grid, (warped_cloth+im)*0.5, im]]
                   
        if (step+1) % opt.display_count == 0:
            board_add_images(board, 'combine', visuals, step+1)
            t = time.time() - iter_start_time
            print('step: %8d, time: %.3f' % (step+1, t), flush=True)
'''


def test_tom(opt, test_loader, model, board):
    device = torch.device('cpu')
    model.to(device)
    # model.cuda()
    model.eval()

    base_name = os.path.basename(opt.checkpoint)
    try_on_dir = os.path.join(os.getcwd(), 'data', 'result')
    if not os.path.exists(try_on_dir):
        os.makedirs(try_on_dir)
    print('Dataset size: %05d!' % (len(test_loader.dataset)), flush=True)
    for step, inputs in enumerate(test_loader.data_loader):
        iter_start_time = time.time()

        im_names = inputs['im_name']
        im = inputs['image'].to(device)
        im_pose = inputs['pose_image']
        im_h = inputs['head']
        shape = inputs['shape']

        agnostic = inputs['agnostic'].to(device)
        c = inputs['cloth'].to(device)
        cm = inputs['cloth_mask'].to(device)

        outputs = model(torch.cat([agnostic, c], 1))
        p_rendered, m_composite = torch.split(outputs, 3, 1)
        p_rendered = F.tanh(p_rendered)
        m_composite = F.sigmoid(m_composite)
        p_tryon = c * m_composite + p_rendered * (1 - m_composite)

        visuals = [[im_h, shape, im_pose],
                   [c, 2*cm-1, m_composite],
                   [p_rendered, p_tryon, im]]

        save_images(p_tryon, im_names, try_on_dir)
        if (step+1) % opt.display_count == 0:
            board_add_images(board, 'combine', visuals, step+1)
            t = time.time() - iter_start_time
            print('step: %8d, time: %.3f' % (step+1, t), flush=True)

    return p_tryon


def viton(stage, data_list):
    # stage : 'GMM' or 'TOM'
    # data_list(list type) 'GMM' : [im_names, c_names]
    # data_list(list type) 'TOM' : [im_names, c_names]
    opt = get_opt(stage, data_list)
    print(opt)
    print("Start to test stage: %s, named: %s!" % (opt.stage, opt.name))

    # create dataset
    train_dataset = CPDataset(opt)

    # create dataloader
    train_loader = CPDataLoader(opt, train_dataset)

    # visualization
    if not os.path.exists(opt.tensorboard_dir):
        os.makedirs(opt.tensorboard_dir)
    board = SummaryWriter(log_dir=os.path.join(opt.tensorboard_dir, opt.name))

    # create model & train
    if opt.stage == 'GMM':
        model = GMM(opt)
        load_checkpoint(model, os.path.join(
            opt.checkpoint, 'gmm_train_new', 'gmm_final.pth'))
        with torch.no_grad():
            test_gmm(opt, train_loader, model, board)
    elif opt.stage == 'TOM':
        model = UnetGenerator(25, 4, 6, ngf=64, norm_layer=nn.InstanceNorm2d)
        load_checkpoint(model, os.path.join(
            opt.checkpoint, 'tom_train_new', 'tom_final.pth'))
        with torch.no_grad():
            test_tom(opt, train_loader, model, board)
    else:
        raise NotImplementedError('Model [%s] is not implemented' % opt.stage)

    print('Finished test %s, named: %s!' % (opt.stage, opt.name))
