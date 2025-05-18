from onvif import ONVIFCamera
from time import sleep
import zeep
from utils.config import CAMERA_CONFIG


class PTZControl:
    wsdl_path = '/home/pi/.local/lib/python3.10/site-packages/wsdl/'

    def __init__(self):
        self.mycam = ONVIFCamera(CAMERA_CONFIG['ip'],
                                 CAMERA_CONFIG['onvif_port'],
                                 CAMERA_CONFIG['usr'],
                                 CAMERA_CONFIG['pwd'],
                                 PTZControl.wsdl_path
                                 )
        self.media = self.mycam.create_media_service()
        self.ptz = self.mycam.create_ptz_service()
        
        zeep.xsd.simple.AnySimpleType.pythonvalue = self.zeep_pythonvalue
        self.media_profile = self.media.GetProfiles()[0]

        self.request = self.ptz.create_type('GetConfigurationOptions')
        self.request.ConfigurationToken = self.media_profile.PTZConfiguration.token
        self.ptz_configuration_options = self.ptz.GetConfigurationOptions(self.request)

        self.request = self.ptz.create_type('ContinuousMove')
        self.request.ProfileToken = self.media_profile.token
        self.ptz.Stop({'ProfileToken': self.media_profile.token})

        if self.request.Velocity is None:
            self.request.Velocity = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position
            self.request.Velocity.PanTilt.space = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            self.request.Velocity.Zoom.space = self.ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

    def zeep_pythonvalue(self, xmlvalue):
        return xmlvalue

    def perform_move(self, timeout):
        # Start continuous move
        self.ptz.ContinuousMove(self.request)
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        self.ptz.Stop({'ProfileToken': self.request.ProfileToken})

    def move_up(self, timeout=0.5):
        self.request.Velocity.PanTilt.x = 0
        self.request.Velocity.PanTilt.y = 0.1
        self.perform_move(timeout)

    def move_down(self, timeout=0.5):
        self.request.Velocity.PanTilt.x = 0
        self.request.Velocity.PanTilt.y = -0.1
        self.perform_move(timeout)

    def move_right(self, timeout=0.5):
        self.request.Velocity.PanTilt.x = 0.1
        self.request.Velocity.PanTilt.y = 0
        self.perform_move(timeout)

    def move_left(self, timeout=0.5):
        self.request.Velocity.PanTilt.x = -0.1
        self.request.Velocity.PanTilt.y = 0
        self.perform_move(timeout)
