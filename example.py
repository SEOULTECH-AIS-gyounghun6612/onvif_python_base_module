from custom_onvif_python import custom_module as c_onvif
import time

IP = # Camera IP address
http_PORT = 80  # Direct Default Port
rtsp_PORT = 554 # Direct Default Port
USER =          # Device ONVIF Username
PASS =          # Device ONVIF Password
DIR_rtsp =   # Device rtsp protocal default stream data directory

ipcamera_controler = c_onvif.IP_CAMERA_control(USER, PASS, IP, http_PORT, DIR_rtsp, rtsp_PORT)
ipcamera_controler.ptz_service_init(0)

# Absolute control example
patrol_points = [
    [1/6, 1.0, 0],
    [1/2, 1.0, 0],
    [5/6, 1.0, 0],
    [-5/6, 1.0, 0],
    [-1/2, 1.0, 0],
    [-1/6, 1.0, 0]]

for _ct, _point in enumerate(patrol_points):
    ipcamera_controler.Absolute_PTZ_control(_point[0], _point[1], _point[2])
    ipcamera_controler.image_capture(dispaly_window=None, save_dir="{}.jpg".format(_ct))
    ipcamera_controler.pause(10)

# Preset control example
Preset_call_number_list = [0, 1, 2]

for _ct, _point in enumerate(Preset_call_number_list):
    ipcamera_controler.Preset_PTZ_control(_point)
    ipcamera_controler.image_capture(dispaly_window=None, save_dir="{}.jpg".format(_ct))
    ipcamera_controler.pause(10)