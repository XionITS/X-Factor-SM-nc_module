import urllib3
import json

from common.input.UserInput import plug_in as userinput
from common.output.model import plug_in as user_db
from common.core.Statistics import chassis_type as chassis_input
from common.core.Statistics import os_type as os_input
from common.core.Statistics import win_ver as win_ver_input



# from common.common.Transform.IdleAssetDataframe import plug_in as idle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())


def daily_plug_in():
    user_asset = userinput()
    #print(user_asset)
    user_input = user_db(user_asset)
    
    #user값 가져와서 통계내기
    #chassis_type
    chassis_input()
    #os
    os_input()
    #windows_ver
    win_ver_input()