import urllib3
import json

from common.input.UserInput import plug_in as userinput
from common.output.model import plug_in as user_db
from common.output.model import plug_in_service as service_db
from common.output.model import plug_in_purchase as purchase_db
from common.output.model import plug_in_security as security_db
from common.core.Statistics import Minutely_statistics, Daily_statistics
# from common.core.Statistics import chassis_type as chassis_input
# from common.core.Statistics import os_type as os_input
# from common.core.Statistics import win_ver as win_ver_input



# from common.common.Transform.IdleAssetDataframe import plug_in as idle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())



def minutely_plug_in():
    user_asset = userinput('common')
    user_input = user_db(user_asset, 'minutely')
    service_asset = userinput('service')
    service_input = service_db(service_asset, 'minutely')
    purchase_asset = userinput('purchase')
    pruchase_input = purchase_db(purchase_asset, 'minutely')
    security_asset = userinput('security')
    security_input = security_db(security_asset, 'minutely')
    # print(security_asset)
    Minutely_statistics()


def daily_plug_in():
    # user_asset = userinput()
    # user_input = user_db(user_asset, 'daily')
    Daily_statistics()


