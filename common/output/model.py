from django.http import HttpResponse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from ..models import *
from .preprocessing import plug_in as PROC


def plug_in(data):
    try:
        #print(data)
        proc_data = PROC(data)
        for d in data:
            hw_list = []
            sw_list = []
            sw_ver_list = []
            hot_list = []
            hotdate_list = []

            for h in range(len(d[9])):
                hw_list.append(d[9][h]['text'])
            for s in range(len(d[10])):
                sw_list.append(d[10][s]['text'])
                sw_ver_list.append(d[11][s]['text'])
            for i in range(len(d[14])):
                hot_list.append(d[14][i]['text'])
                hotdate_list.append(d[15][i]['text'])
            xfactor_user = XFactor_User()
            xfactor_user_log = XFactor_User_log()
            computer_id = d[0][0]['text']
            defaults = {
                'computer_name': d[1][0]['text'],
                'ip_address': d[2][0]['text'],
                'mac_address': d[3][0]['text'],
                'chasisstype': d[4][0]['text'],
                'os_simple': d[5][0]['text'],
                'os_total': d[6][0]['text'],
                'os_version': d[7][0]['text'],
                'os_build': d[8][0]['text'],
                'hw_list': str(hw_list).replace('"','').replace(",","<br>").replace('\'','').replace('[','').replace(']',''),
                'sw_list': str(sw_list).replace('"','').replace('!','<br>').replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_ver_list': str(sw_ver_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'hotfix': str(hot_list).replace("''", '').replace("' ", '').replace("'", '').replace(",", "<br>").replace('[', '').replace(']', ''),
                'hotfix_date': str(hotdate_list).replace("''", '').replace("' ", '').replace("'", '').replace(",", "<br>").replace('[', '').replace(']', '')
            }
            xfactor_user, created = XFactor_User.objects.update_or_create(computer_id=computer_id, defaults=defaults)
            xfactor_user_log = XFactor_User_log.objects.create(computer_id=computer_id, **defaults)

            xfactor_user.save()
            xfactor_user_log.save()
    except Exception as e:
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

