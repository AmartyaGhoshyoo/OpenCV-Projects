"""
Pycaw is a Python library designed exclusively for controlling audio devices on Windows systems.
It allows programmatic access to audio sessions, volume control, and sound device management on the Windows platform.
Note: Pycaw does not support macOS or Linux. It is built specifically for Windows using Core Audio APIs.
If you're looking for similar functionality on other platforms, you'll need alternative libraries.   
pip install pycaw 
"""
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
print(volume.GetVolumeRange())# so basically it gives the range of the minimu and max volume which we give in the 'SetMasterVolumeLevel'
volume.SetMasterVolumeLevel(-15.0, None)