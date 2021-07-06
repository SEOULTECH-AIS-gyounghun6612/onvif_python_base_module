from onvif import ONVIFCamera
import cv2
import time


class IP_CAMERA_control():
    def __init__(self, USER, PASSWORD, IP, http_PORT, DIR_rtsp, rtsp_PORT, DIR_wsdl=None):
        """
        Detail
        paramerts:
            USER    :
            PASSWORD:
            IP      :
            PORT    :
            DIR_wsdl:
            ADRESS_rtsp:
        """
        if DIR_wsdl is not None:
            self.cam = ONVIFCamera(IP, http_PORT, USER, PASSWORD, DIR_wsdl)
        else:
            self.cam = ONVIFCamera(IP, http_PORT, USER, PASSWORD, "./wsdl")

        self.ADRESS_rtsp = \
            "rtsp://{}:{}@{}:{}/{}".format(USER, PASSWORD, IP, rtsp_PORT, DIR_rtsp)
        self.media_profiles = self.cam.create_media_service().GetProfiles()

    def ptz_service_init(self, profile_num):
        """
        Detail
        paramerts:
            profile_num:
        """
        self.ptz = self.cam.create_ptz_service()
        self.ptz_controol_active = False
        selected_PF = self.media_profiles[profile_num]

        get_PTZ_CONGIF_RQ = self.ptz.create_type('GetConfigurationOptions')
        get_PTZ_CONGIF_RQ.ConfigurationToken = \
            selected_PF.PTZConfiguration.token
        PTZ_CONGIF_OPT = self.ptz.GetConfigurationOptions(get_PTZ_CONGIF_RQ)
        
        # Preset_list init
        self.Preset_list = self.ptz.GetPresets(selected_PF.token)

        # RelativeMove_Requset init
        self.R_Move_RQ = self.ptz.create_type('RelativeMove')
        self.R_Move_RQ.ProfileToken = selected_PF.token
        if self.R_Move_RQ.Translation is None:
            self.R_Move_RQ.Translation = \
                self.ptz.GetStatus({'ProfileToken': selected_PF.token}).Position
            self.R_Move_RQ.Translation.PanTilt.space = \
                PTZ_CONGIF_OPT.Spaces.RelativePanTiltTranslationSpace[0].URI
            self.R_Move_RQ.Translation.Zoom.space = \
                PTZ_CONGIF_OPT.Spaces.RelativeZoomTranslationSpace[0].URI

        # AbsoluteMove_Request init
        self.A_Move_RQ = self.ptz.create_type('AbsoluteMove')
        self.A_Move_RQ.ProfileToken = selected_PF.token
        if self.A_Move_RQ.Position is None:
            self.A_Move_RQ.Position = \
                self.ptz.GetStatus({'ProfileToken': selected_PF.token}).Position
            self.A_Move_RQ.Position.PanTilt.space = \
                PTZ_CONGIF_OPT.Spaces.AbsolutePanTiltPositionSpace[0].URI
            self.A_Move_RQ.Position.Zoom.space = \
                PTZ_CONGIF_OPT.Spaces.AbsoluteZoomPositionSpace[0].URI

        # ContinousMove_Request init
        C_Move_RQ = self.ptz.create_type('ContinuousMove')
        C_Move_RQ.ProfileToken = selected_PF.token
        if C_Move_RQ.Velocity is None:
            C_Move_RQ.Velocity = \
                self.ptz.GetStatus({'ProfileToken': selected_PF.token}).Position
            C_Move_RQ.Velocity.PanTilt.space = \
                PTZ_CONGIF_OPT.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            C_Move_RQ.Velocity.Zoom.space = \
                PTZ_CONGIF_OPT.Spaces.ContinuousZoomVelocitySpace[0].URI

        # Relative Translation Paramert
        self.PTZ_R_MOVE = 0
        self.Max_R_P = PTZ_CONGIF_OPT.Spaces.RelativePanTiltTranslationSpace[0].XRange.Max
        self.Min_R_P = PTZ_CONGIF_OPT.Spaces.RelativePanTiltTranslationSpace[0].XRange.Min
        self.MAX_R_T = PTZ_CONGIF_OPT.Spaces.RelativePanTiltTranslationSpace[0].YRange.Max
        self.MIN_R_T = PTZ_CONGIF_OPT.Spaces.RelativePanTiltTranslationSpace[0].YRange.Min
        self.MAX_R_Z = PTZ_CONGIF_OPT.Spaces.RelativeZoomTranslationSpace[0].XRange.Max
        self.MIN_R_Z = PTZ_CONGIF_OPT.Spaces.RelativeZoomTranslationSpace[0].XRange.Min

        # Apsolute Position Paramert
        self.PTZ_A_MOVE = 1
        self.MAX_A_P = PTZ_CONGIF_OPT.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Max
        self.MIN_A_P = PTZ_CONGIF_OPT.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Min
        self.MAX_A_T = PTZ_CONGIF_OPT.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Max
        self.MIN_A_T = PTZ_CONGIF_OPT.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Min
        self.MAX_A_Z = PTZ_CONGIF_OPT.Spaces.AbsoluteZoomPositionSpace[0].XRange.Max
        self.MIN_A_Z = PTZ_CONGIF_OPT.Spaces.AbsoluteZoomPositionSpace[0].XRange.Min

        # Continous Velocity Limit
        self.PTZ_C_MOVE = 2
        # XMAX = PTZ_CONGIF_OPT.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
        # XMIN = PTZ_CONGIF_OPT.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
        # YMAX = PTZ_CONGIF_OPT.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
        # YMIN = PTZ_CONGIF_OPT.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

    def set_A_MOVE_RQ(self, P, T, Z):
        PAN_POSITION = \
            self.MAX_A_P if self.MAX_A_P < P else (self.MIN_A_P if self.MIN_A_P > P else P)
        TILT_POSITION = \
            self.MAX_A_T if self.MAX_A_T < T else (self.MIN_A_T if self.MIN_A_T > T else T)
        ZOOM_POSITION = \
            self.MAX_A_Z if self.MAX_A_Z < Z else (self.MIN_A_Z if self.MIN_A_Z > Z else Z)

        print('move to {} {} {}'.format(PAN_POSITION, TILT_POSITION, ZOOM_POSITION))
        return [PAN_POSITION, TILT_POSITION, ZOOM_POSITION]

    def set_R_MOVE_RQ(self):
        pass

    def set_C_MOVE_RQ(self):
        pass

    def PTZ_MOVE(self, RQ, MODE=1):
        if self.ptz_controol_active:
            # before PTZ control shut down
            self.PTZ_STOP(RQ)

        if MODE == self.PTZ_R_MOVE:  # RelativeMove
            self.ptz.RelativeMove(RQ)
            self.ptz_controol_active = True
        elif MODE == self.PTZ_A_MOVE:  # RelativeMove
            self.ptz.AbsoluteMove(RQ)
            self.ptz_controol_active = True
        elif MODE == self.PTZ_G_P:    # Go to Preset
            self.ptz.GotoPreset(RQ)
            self.ptz_controol_active = True

        else:
            print("!!! ERROR!!! Selected Mode not Supported.")

    def Absolute_PTZ_control(self, P, T, Z):
        position = self.set_A_MOVE_RQ(P, T, Z)
        self.A_Move_RQ.Position.PanTilt.x = position[0]
        self.A_Move_RQ.Position.PanTilt.y = position[1]
        self.A_Move_RQ.Position.Zoom.x = position[2]

        self.PTZ_MOVE(self.A_Move_RQ, MODE=self.PTZ_A_MOVE)

    def Preset_PTZ_control(self, Preset_num):
        Preset_data = self.Preset_list[Preset_num]["PTZPosition"]
        _P = Preset_data["PanTilt"].x
        _T = Preset_data["PanTilt"].y
        _Z = Preset_data["Zoom"].x
        self.Absolute_PTZ_control(_P, _T, _Z)


    def PTZ_STOP(self, RQ):
        self.ptz.Stop({'ProfileToken': RQ.ProfileToken})
        self.ptz_controol_active = False

    # Stream function
    def image_capture(self, dispaly_window="capture", save_dir=None):
        ip_videocapture = cv2.VideoCapture(self.ADRESS_rtsp)
        ret, frame = ip_videocapture.read()
        if ret:
            if save_dir is not None:
                cv2.imwrite(save_dir, frame)
            if dispaly_window is not None:
                cv2.imshow(dispaly_window, frame)
        return ret, frame

    @staticmethod
    def waitKey(ms):
        return cv2.waitKey(ms)

    @staticmethod
    def pause(ms):
        time.sleep(ms/1000)
