# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:17:17 2020

@author: MA
"""
import nibabel as nib
import nnunet.inference.myvi
import numpy as np
import scipy.ndimage as ndimg
import argparse
import os

if __name__ == "__main__":
    # get img data and spacing
    output_folder = 'E:\\nnU-Net_v2\\nnUNet_predict1'
    filepath = os.path.dirname(output_folder)
    filepath1 = os.path.basename(output_folder)
    filepath2 = os.path.join(filepath, filepath1)
    filepath3 = os.listdir(output_folder)
    ct_image_file_list = os.path.join(filepath2, filepath3[0])
    # get img data and spacing
    nii = nib.load(ct_image_file_list)
    imgs = nii.get_data() # 3D matrix; imgs.shape = (x,y,z)
    # if you do not know the spacing information, just set zoom = (1.0, 1.0, 1.0)
    zoom = nii.header.get_zooms()
    # smooth (may loss details)
    manager = nnunet.inference.myvi.Manager()
    a = np.sum(imgs == 1)
    if a!=0:
        organ_1 = ndimg.gaussian_filter(np.float32(imgs == 1), 1)
        vts, fs, ns, vs = nnunet.inference.myvi.util.build_surf3d(organ_1, 1, 0.5, zoom)
        manager.add_surf('spleen', vts, fs, ns, (1, 0, 0))

    b1 = np.sum(imgs == 2)
    if b1 != 0:
        organ_2 = ndimg.gaussian_filter(np.float32(imgs == 2), 1)
        vts2, fs2, ns2, vs2 = nnunet.inference.myvi.util.build_surf3d(organ_2, 1, 0.5, zoom)
        manager.add_surf('pancreas', vts2, fs2, ns2, (0, 1, 0))

    c1 = np.sum(imgs == 3)
    if c1 != 0:
        organ_3 = ndimg.gaussian_filter(np.float32(imgs == 3), 1)
        vts3, fs3, ns3, vs3 = nnunet.inference.myvi.util.build_surf3d(organ_3, 1, 0.5, zoom)
        manager.add_surf('liver', vts3, fs3, ns3, (0, 0, 1))
    # vts, fs, ns, cs are nodes，surface，normal vector, and color respectively
    manager.show('Organ 3D Demo')








