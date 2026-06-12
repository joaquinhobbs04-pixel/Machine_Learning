import numpy as np
import os
import nibabel as nb
from os import listdir

path = 'E:\\nnU-Net_v2\\nnUNet_raw\\Task10_Aorta_Segmentation\\test_images1' #输入文件夹路径
filename = listdir(path)
print(filename)

mask = [0,1,2,3]
for v in mask:
    print("Volume of "+str(v)+"  voxel: ")
    for fl in filename:
        file_path = os.path.join(path, fl)
        nii = nb.load(file_path)
        img = nii.get_fdata()

        voxel_dims = (nii.header["pixdim"])[1:4]
        nonzero_voxel_count = np.count_nonzero(img)
        tmp={}
        for k in mask:
            tmp[k] = np.sum(img == k)

        voxel_volume = np.prod(voxel_dims)
        print(tmp[v] * voxel_volume)


