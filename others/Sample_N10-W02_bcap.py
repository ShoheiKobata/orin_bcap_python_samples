# coding:utf-8

# This is a sample program to get the image of N10-W02 using bCAP communication.
#
#

import os
from PIL import Image, ImageOps
import io
import numpy as np
import cv2
import pybcapclient.bcapclient as bcap

# プロキシ設定を無視する。
if os.environ.get("https_proxy"):
    del os.environ["https_proxy"]
if os.environ.get("http_proxy"):
    del os.environ["http_proxy"]

# Setting COBOTTA IP Address
host = "192.168.0.1"
port = 5007
timeout = 2000

mbcapclient = bcap.BCAPClient(host,port,timeout)
mbcapclient.service_start("")

# Server = N10-W02 IP Address
hCameraCtrl = mbcapclient.controller_connect('',"CaoProv.Canon.N10-W02", "", "Server=192.168.0.90")

# FiIRMWARE
hFirmware = mbcapclient.controller_getvariable(hCameraCtrl,"@FIRMWARE")
print(mbcapclient.variable_getvalue(hFirmware))

himage = mbcapclient.controller_getvariable(hCameraCtrl,'IMAGE')

while(1):
    image_row = mbcapclient.variable_getvalue(himage)
    # print(type(image_row))

    img_binarystream = io.BytesIO(image_row)
    img_pil = Image.open(img_binarystream)
    # print(img_pil.mode)
    w,h = img_pil.size
    # print(img_pil.size)
    img_numpy = np.array(img_pil)
    img_numpy_bgr = cv2.cvtColor(img_numpy,cv2.COLOR_RGBA2BGR)
    resize_img_numpy_bgr = cv2.resize(img_numpy_bgr,(int(w/2),int(h/2)))

    cv2.imshow('Image',resize_img_numpy_bgr)
    #ESCキーでブレーク
    if cv2.waitKey(20) & 0xFF == 27:
        break