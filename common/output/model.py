from django.http import HttpResponse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from ..models import *
from .preprocessing import plug_in as PROC
import pytz
from datetime import datetime, timedelta

def plug_in(data, time):
    try:
        #print(data)
        proc_data = PROC(data)
        for d in data:
            #hw_list = []
            sw_list = []
            sw_ver_list = []
            sw_ver_install_list = []
            sw_ver_lastrun_list = []
            hot_list = []
            hotdate_list = []
            # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
            local_tz = pytz.timezone('Asia/Seoul')
            # UTC 시간대를 사용하여 현재 시간을 얻음
            utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
            # 현재 시간대로 시간 변환
            now = utc_now.astimezone(local_tz)
            # for h in range(len(d[9])):
            #     hw_list.append(d[9][h]['text'])
            for s in range(len(d[14])):
                sw_list.append(d[14][s]['text'])
                sw_ver_list.append(d[15][s]['text'])
                sw_ver_install_list.append(d[16][s]['text'])
                sw_ver_lastrun_list.append(d[17][s]['text'])
            for i in range(len(d[20])):
                hot_list.append(d[20][i]['text'])
                hotdate_list.append(d[21][i]['text'])
            # xfactor_user = Xfactor_Common()
            # xfactor_user_log = Xfactor_Common_log()
            computer_id = d[0][0]['text']
            defaults = {
                'computer_name': d[1][0]['text'],
                'ip_address': d[2][0]['text'],
                'mac_address': d[3][0]['text'],
                'chassistype': d[4][0]['text'],
                'os_simple': d[5][0]['text'],
                'os_total': d[6][0]['text'],
                'os_version': d[7][0]['text'],
                'os_build': d[8][0]['text'],
                'hw_cpu' : d[9][0]['text'],
                'hw_ram' : d[10][0]['text'],
                'hw_mb' : d[11][0]['text'],
                'hw_disk' : d[12][0]['text'],
                'hw_gpu' : d[13][0]['text'],
                #'hw_list': str(hw_list).replace('"','').replace(",","<br>").replace('\'','').replace('[','').replace(']',''),
                'sw_list': str(sw_list).replace('"','').replace('!','<br>').replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_ver_list': str(sw_ver_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_install' : str(sw_ver_install_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_lastrun' : str(sw_ver_lastrun_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'first_network' : d[18][0]['text'],
                'last_network' : d[19][0]['text'],
                'hotfix': str(hot_list).replace("''", '').replace("' ", '').replace("'", '').replace(",", "<br>").replace('[', '').replace(']', ''),
                'hotfix_date': str(hotdate_list).replace("''", '').replace("' ", '').replace("'", '').replace(",", "<br>").replace('[', '').replace(']', ''),
                'user_date' : now
            }
            if time == 'minutely' :
                xfactor_user, created = Xfactor_Common.objects.update_or_create(computer_id=computer_id, defaults=defaults)
                xfactor_user.save()
            else :
                xfactor_user_log = Xfactor_Common_log.objects.create(computer_id=computer_id, **defaults)
                xfactor_user_log.save()
    except Exception as e:
        print(d)
        print(e)
    return HttpResponse("Data saved successfully!")
        # xfactor_user = XFactor_User(
        # computer_id = d[0][0]['text'],
        # computer_name = d[1][0]['text'],
        # ip_address = d[2][0]['text'],
        # mac_address = d[3][0]['text'],
        # chasisstype = d[4][0]['text'],
        # os_simple = d[5][0]['text'],
        # os_total = d[6][0]['text'],
        # os_version = d[7][0]['text'],
        # os_build = d[8][0]['text'],
        # hw_list = d[9][0]['text'],
        # sw_list = d[10][0]['text'])
        # xfactor_user.save()

