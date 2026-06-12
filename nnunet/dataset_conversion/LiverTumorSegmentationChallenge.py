#    Copyright 2019 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from collections import OrderedDict
import SimpleITK as sitk
from batchgenerators.utilities.file_and_folder_operations import *
import multiprocessing
from multiprocessing import Pool
import numpy as np
from scipy.ndimage import label


def export_segmentations(indir, outdir):
    niftis = subfiles(indir, suffix='nii.gz', join=False)
    for n in niftis:
        identifier = str(n.split("_")[-1][:-7])
        outfname = join(outdir, "test-segmentation-%s.nii" % identifier)
        img = sitk.ReadImage(join(indir, n))
        sitk.WriteImage(img, outfname)


def export_segmentations_postprocess(indir, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    niftis = subfiles(indir, suffix='nii.gz', join=False)
    for n in niftis:
        print("\n", n)
        identifier = str(n.split("_")[-1][:-7])
        outfname = join(outdir, "test-segmentation-%s.nii" % identifier)
        img = sitk.ReadImage(join(indir, n))
        img_npy = sitk.GetArrayFromImage(img)
        lmap, num_objects = label((img_npy > 0).astype(int))
        sizes = []
        for o in range(1, num_objects + 1):
            sizes.append((lmap == o).sum())
        mx = np.argmax(sizes) + 1
        print(sizes)
        img_npy[lmap != mx] = 0
        img_new = sitk.GetImageFromArray(img_npy)
        img_new.CopyInformation(img)
        sitk.WriteImage(img_new, outfname)


def load_save_train(args):
    data_file, seg_file, img_dir, lab_dir = args

    pat_id_data = data_file.split("\\")[-1]
    pat_id_data = pat_id_data[:-13]
    img_itk = sitk.ReadImage(data_file)
    sitk.WriteImage(img_itk, join(img_dir, pat_id_data + "_0000.nii.gz"))

    pat_id_seg = seg_file.split("\\")[-1]
    pat_id_seg = pat_id_seg[:-13]
    img_itk = sitk.ReadImage(seg_file)
    sitk.WriteImage(img_itk, join(lab_dir, pat_id_seg + ".nii.gz"))
    return pat_id_data, pat_id_seg


def load_save_test(args):
    data_file, img_dir_te = args
    pat_id = data_file.split("\\")[-1]
    pat_id = pat_id[:-13]
    img_itk = sitk.ReadImage(data_file)
    sitk.WriteImage(img_itk, join(img_dir_te, pat_id + "_0000.nii.gz"))
    return pat_id


if __name__ == "__main__":
    multiprocessing.freeze_support()

    train_labels_dir = "D:\\xiongxiangyu\\nnU-Net_v2\\nnUnet_raw\\Task10_Aorta_Segmentation\\train_labels"
    train_images_dir = "D:\\xiongxiangyu\\nnU-Net_v2\\nnUnet_raw\\Task10_Aorta_Segmentation\\train_images"
    test_images_dir = "D:\\xiongxiangyu\\nnU-Net_v2\\nnUnet_raw\\Task10_Aorta_Segmentation\\test_images"

    output_folder = "D:\\xiongxiangyu\\nnU-Net_v2\\nnUNet_raw_splitted\\Task10_Aorta_Segmentation"
    img_dir = join(output_folder, "imagesTr")
    lab_dir = join(output_folder, "labelsTr")
    img_dir_te = join(output_folder, "imagesTs")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    if not os.path.exists(lab_dir):
        os.makedirs(lab_dir)
    if not os.path.exists(img_dir_te):
        os.makedirs(img_dir_te)
    img_dirs = [img_dir for i in os.listdir(train_images_dir)]
    lab_dirs = [lab_dir for i in os.listdir(train_labels_dir)]
    img_dir_tes = [img_dir_te for i in os.listdir(test_images_dir)]

    nii_files_tr_data = subfiles(train_images_dir, True, None, "nii.gz", True)
    nii_files_tr_seg = subfiles(train_labels_dir, True, None, "nii.gz", True)
    nii_files_ts = subfiles(test_images_dir, True, None, "nii.gz", True)

    p = Pool(4)
    train_ids = p.map(load_save_train, zip(nii_files_tr_data, nii_files_tr_seg, img_dirs, lab_dirs))
    test_ids = p.map(load_save_test, zip(nii_files_ts, img_dir_tes))
    p.close()
    p.join()

    json_dict = OrderedDict()
    json_dict['name'] = "LITS"
    json_dict['description'] = "LITS"
    json_dict['tensorImageSize'] = "4D"
    json_dict['reference'] = "see challenge website"
    json_dict['licence'] = "see challenge website"
    json_dict['release'] = "0.0"
    json_dict['modality'] = {
        "0": "CT"
    }

    json_dict['labels'] = {
        "0": "background",
        "1": "aorta",
        "2": "true_lumen",
        "3": "false_lumen",
    }

    json_dict['numTraining'] = len(train_ids)
    json_dict['numTest'] = len(test_ids)
    json_dict['training'] = [
        {'image': "D:\\xiongxiangyu\\nnU-Net_v2\\nnUNet_raw_splitted\\Task10_Aorta_Segmentation\\imagesTr\\%s.nii.gz" % i[0],
         "label": "D:\\xiongxiangyu\\nnU-Net_v2\\nnUNet_raw_splitted\\Task10_Aorta_Segmentation\\imagesTs\\%s.nii.gz" % i[1]}
        for i in train_ids]
    json_dict['test'] = \
        ["D:\\xiongxiangyu\\nnU-Net_v2\\nnUNet_raw_splitted\\Task10_Aorta_Segmentation\\labelsTr\\%s.nii.gz"
                         % i for i in test_ids]
    with open(os.path.join(output_folder, "dataset.json"), 'w') as f:
        json.dump(json_dict, f, indent=4, sort_keys=True)