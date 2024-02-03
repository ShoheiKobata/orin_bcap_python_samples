#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyrealsense2 as rs
import numpy as np
import cv2
from logging import INFO, getLogger, NullHandler


class RealsenseCtrl():
    """RealSense class

    Attributes:
        connected_serial (list): List of connected RealSense serials. Get with get_info function
        connected_asic_serial_number (list): List of connected RealSense serials. Get with get_info function

    """
    def __init__(self):
        # set logger
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(INFO)
        self._logger.propagate = True
        self._logger.info('init camera')
        self.is_connected = False
        self.conf_dict = {}
        # decimarion_filterのパラメータ
        self.decimate = rs.decimation_filter()
        self.decimate.set_option(rs.option.filter_magnitude, 1)
        # spatial_filterのパラメータ
        self.spatial = rs.spatial_filter()
        self.spatial.set_option(rs.option.filter_magnitude, 1)
        self.spatial.set_option(rs.option.filter_smooth_alpha, 0.25)
        self.spatial.set_option(rs.option.filter_smooth_delta, 50)
        # hole_filling_filterのパラメータ
        self.hole_filling = rs.hole_filling_filter(1)
        # disparity
        self.depth_to_disparity = rs.disparity_transform(True)
        self.disparity_to_depth = rs.disparity_transform(False)
    # End def

    def get_info(self):
        """接続されいているリアルセンスの情報を取得

        接続されいているリアルセンスの情報を取得
        connected_serial , connected_asic_serial_number が更新されます。
        """
        self.connected_serial = []
        self.connected_asic_serial_number = []
        ctx = rs.context()
        self.devices = ctx.query_devices()
        for device in self.devices:  # pyrealsense2.device
            self.connected_serial.append(device.get_info(rs.camera_info.serial_number))
            self.connected_asic_serial_number.append(device.get_info(rs.camera_info.asic_serial_number))
        return self.connected_serial
    # End def

    def connect_rs(self, serial='', width=1280, height=720):
        # init streaming
        config = (rs.config())
        if not serial == '':
            config.enable_device(serial)
        # End if
        config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
        # Start streaming
        pipline = rs.pipeline()
        profile = pipline.start(config)
        # 距離[m] = depth * depth_scale
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        # set align
        align_to = rs.stream.color
        align = rs.align(align_to)
        info_dict = {'width': width, 'height': height, 'config': config, 'pipline': pipline, 'profile': profile, 'align': align, 'depth_scale': depth_scale}
        self.conf_dict[serial] = info_dict
        # configsの配列インデックスを返す
        return self.conf_dict
    # End def

    def get_rgbd_img(self, serial=''):
        enable_filtter = True
        if serial == '':
            return False, False, False, False
        else:
            info = self.conf_dict[serial]
        # End if
        # wait frame (color and depth)
        frames = info['pipline'].wait_for_frames()
        aligned_frames = info['align'].process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if not depth_frame or not color_frame:
            return False, False, False, False
        # End if
        # Filttering
        if enable_filtter:
            filter_frame = depth_frame
            '''
            filter_frame = self.decimate.process(depth_frame)
            filter_frame = self.depth_to_disparity.process(filter_frame)
            filter_frame = self.spatial.process(filter_frame)
            filter_frame = self.disparity_to_depth.process(filter_frame)
            '''
            filter_frame = self.hole_filling.process(filter_frame)
            result_frame = filter_frame.as_depth_frame()
        else:
            result_frame = depth_frame
        # change imageto numpy array
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(result_frame.get_data())
        # change depth image to colormap
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.08), cv2.COLORMAP_JET)
        return True, color_image, depth_image, depth_colormap
    # End def

    def crop_image_distance(self, serial, clop_distance_m, color_image, depth_image):
        if serial == '':
            return False, False, False, False
        else:
            info = self.conf_dict[serial]
        # End if
        bg_image = np.zeros((info['height'], info['width'], 3), dtype=np.uint8)
        bg_image += [np.uint8(0), np.uint8(255), np.uint8(0)][:: -1]  # RGBで緑指定
        crop_distance = clop_distance_m / info['depth_scale']
        depth_filtered_image = (depth_image < crop_distance) * depth_image
        # depth_gray_filtered_image = (depth_filtered_image * 255. / crop_distance).reshape((info['height'], info['width'])).astype(np.uint8)
        # 指定距離以上を無視したRGB画像
        color_filtered_image = (depth_filtered_image.reshape((info['height'], info['width'], 1)) > 0) * color_image
        background_masked_image = (depth_filtered_image.reshape((info['height'], info['width'], 1)) == 0) * bg_image
        composite_image = background_masked_image + color_filtered_image
        return True, composite_image
    # End def

    def finish_all(self):
        for serial in self.conf_dict.keys():
            info = self.conf_dict[serial]
            info['pipline'].stop()
        # End def
    # End def

    def __del__(self):
        '''デストラクタ
        デストラクタ 終了処理
        '''
        self.finish_all()
        print('finish')
    # End def

# End class


def main():
    rs_ctrl = RealsenseCtrl()
    serials = rs_ctrl.get_info()
    print(serials)
    rs_ctrl.connect_rs(serials[0])
    while True:
        ret = False
        ret2 = False
        # 表示
        ret, color_image, depth_image, depth_colormap = rs_ctrl.get_rgbd_img(serials[0])
        if ret:
            ret2, composite_image = rs_ctrl.crop_image_distance(serials[0], clop_distance_m=1.2, color_image=color_image, depth_image=depth_image)
        if ret2:
            cv2.namedWindow('demo', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('demo', composite_image)

        if cv2.waitKey(1) & 0xff == 27:
            break
# End def


if __name__ == '__main__':
    main()
# End
