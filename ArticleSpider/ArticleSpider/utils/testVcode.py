# -*- coding: utf-8 -*-

# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
# from PIL import Image
#
# image = Image.open('./captcha.gif')
#
# vcode = pytesseract.image_to_string(image)
#
# print (vcode)

# import ctypes
#
# DLL_PATH = 'C:\Program Files\Tesseract-OCR/libtesseract-3.dll'
# TESSDATA_PREFIX = b'./tessdata'
# lang = b'eng'
#
# tesseract = ctypes.cdll.LoadLibrary(DLL_PATH)
# tesseract.TessBaseAPICreate.restype = ctypes.c_uint64
# api = tesseract.TessBaseAPICreate()
# rc = tesseract.TessBaseAPIInit3(ctypes.c_uint64(api), TESSDATA_PREFIX, lang)
# if rc:
#     tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
#     print('Could not initialize tesseract.\n')
#     exit(3)
#
# def from_file(path):
#     tesseract.TessBaseAPIProcessPages(
#         ctypes.c_uint64(api), path, None, 0, None)
#     tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
#     text_out = tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(api))
#     return ctypes.string_at(text_out)
#
# if __name__ == '__main__':
#     image_file_path = b'./captcha.tif'
#     result = from_file(image_file_path)
#     print(result)
#

import os
import subprocess


def image_to_string(img, cleanup=True, plus=''):
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    subprocess.check_output('tesseract ' + img + ' ' +
                            img + ' ' + plus, shell=True)  # 生成同名txt文件
    text = ''
    with open(img + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text

print(image_to_string('./6.gif', True))