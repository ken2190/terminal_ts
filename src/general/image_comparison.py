import os
from PIL import Image
from PIL import ImageFile
import imagehash
import math
#使用第三方库：Pillow
import operator
from functools import reduce


def get_path():
    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path = path + "\\resource\\"
    return path

def compare_image(img_file1, img_file2):
    """
    仅适用于完全相同的图片比较
    """
    if img_file1 == img_file2:
        return True
    fp1 = open(img_file1, 'rb')
    fp2 = open(img_file2, 'rb')

    img1 = Image.open(fp1)
    img2 = Image.open(fp2)

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    b = img1 == img2

    fp1.close()
    fp2.close()

    return b


def get_hash_dict(dir):
    hash_dict = {}
    image_quantity = 0
    for _, _, files in os.walk(dir):
        for i, fileName in enumerate(files):
            with open(dir + fileName, 'rb') as fp:
                hash_dict[dir + fileName] = imagehash.average_hash(Image.open(fp))
                image_quantity += 1

    return hash_dict, image_quantity


def compare_image_with_hash(image_file_name_1, image_file_name_2, max_dif):
    """
    max_dif: 允许最大hash差值, 越小越精确,最小为0
    推荐使用
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = None
    hash_2 = None
    with open(image_file_name_1, 'rb') as fp:
        hash_1 = imagehash.average_hash(Image.open(fp))
    with open(image_file_name_2, 'rb') as fp:
        hash_2 = imagehash.average_hash(Image.open(fp))
    dif = hash_1 - hash_2
    if dif < 0:
        dif = -dif
    if dif <= max_dif:
        return True
    else:
        return False

def compare_image_with_histogram(image_file_name_1, image_file_name_2):
    """
    在compare_image_with_hash 基础上优化的方法，差别较小的值应在100以内
    推荐使用
    """
    image1 = Image.open(image_file_name_1)
    image3 = Image.open(image_file_name_2)
    h1 = image1.histogram()
    h2 = image3.histogram()

    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    print("对比差值：",result)
    if result < 11000:
        print("对比基本相似")
        return True
    else:
        print("不一致")
        return False

def compare_image_dir_with_hash(dir_1, dir_2, max_dif=0):
    """
    max_dif: 允许最大hash差值, 越小越精确,最小为0
    用于比较两个文件夹内的图片
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_dict_1, image_quantity_1 = get_hash_dict(dir_1)
    hash_dict_2, image_quantity_2 = get_hash_dict(dir_2)

    if image_quantity_1 > image_quantity_2:
        tmp = image_quantity_1
        image_quantity_1 = image_quantity_2
        image_quantity_2 = tmp

        tmp = hash_dict_1
        hash_dict_1 = hash_dict_2
        hash_dict_2 = tmp

    result_dict = {}

    for k in hash_dict_1.keys():
        result_dict[k] = None

    for dif_i in range(0, max_dif + 1):
        have_none = False

        for k_1 in result_dict.keys():
            if result_dict.get(k_1) is None:
                have_none = True

        if not have_none:
            return result_dict

        for k_1, v_1 in hash_dict_1.items():
            for k_2, v_2 in hash_dict_2.items():
                sub = (v_1 - v_2)
                if sub < 0:
                    sub = -sub
                if sub == dif_i and result_dict.get(k_1) is None:
                    result_dict[k_1] = k_2
                    break
    return result_dict

# if __name__ == "__mian__":
#     path = r"C:\Users\Administrator\Desktop\py-test\terminal_ts\resource\image\setting\\"
#     a = path+'Screenshot.png'
#     b = path + 'Screenshot1.jpg'
#     compare_image_with_histogram(a, b)  # 用于图片是否大致一致对比（6为像素点）
    # print(compare_image('IMG_20180827_102255.jpg', 'IMG_20180827_102257.jpg'))                              # 用于图片是否完全一致对比
    # r = compare_image_dir_with_hash('image1\\', image2\\', 10)                                              # 用户目录下拖的对比
    # for k in r.keys():
    #     print(k, r.get(k))
