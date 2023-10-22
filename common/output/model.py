from django.http import HttpResponse
import os

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from ..models import *
from .preprocessing import plug_in as PROC
import pytz
from datetime import datetime, timedelta

def plug_in_minutely(data):
    try:
        #print(data)
        # Xfactor_Service.objects.all().delete()
        # Xfactor_Purchase.objects.all().delete()
        # Xfactor_Security.objects.all().delete()
        # Xfactor_Common.objects.all().delete()
        proc_data = PROC(data)
        for d in proc_data:
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
                'os_total': d[6][0]['text'].replace('Microsoft ', ''),
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
                'subnet' : d[22][0]['text'],
                'essential1': d[23][0]['text'],
                'essential2': d[24][0]['text'],
                'essential3': d[25][0]['text'],
                'essential4': d[26][0]['text'],
                'essential5': d[27][0]['text'],
                'mem_use': d[28][0]['text'],
                'disk_use': d[29][0]['text'],
                't_cpu': d[30][0]['text'],
                'logged_name': d[31][0]['text'].replace('NC-KOREA\\',''),
                'user_date' : now
            }
            xfactor_common, created = Xfactor_Common.objects.update_or_create(computer_id=computer_id, defaults=defaults)
            # xfactor_common.save()
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

# def plug_in_service(data):
#
#     # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
#     local_tz = pytz.timezone('Asia/Seoul')
#     # UTC 시간대를 사용하여 현재 시간을 얻음
#     utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
#     # 현재 시간대로 시간 변환
#     now = utc_now.astimezone(local_tz)
#     #now = now.replace(minute=0, second=0, microsecond=0)
#     proc_data = PROC(data)
#     for d in proc_data:
#         computer_id = d[0][0]['text']
#         try:
#             common_id = Xfactor_Common.objects.get(computer_id=computer_id)
#         except Exception as e:
#             print(computer_id)
#             print(e)
#             print("미닛틀리 예외발생")
#             continue  # 다음 for문으로 넘어감
#         defaults = {
#             'essential1': d[1][0]['text'],
#             'essential2': d[2][0]['text'],
#             'essential3': d[3][0]['text'],
#             'essential4': d[4][0]['text'],
#             'essential5': d[5][0]['text'],
#             'subnet': d[6][0]['text'],
#             'mem_use': d[7][0]['text'],
#             'disk_use': d[8][0]['text'],
#             't_cpu': d[9][0]['text'],
#             'user_date': now
#         }
#         computer_id = common_id.computer_id
#         xfactor_service, created = Xfactor_Service.objects.update_or_create(computer_id=computer_id, defaults=defaults)
#     return HttpResponse("Data saved successfully!")


def plug_in_purchase(data):
    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    now = utc_now.astimezone(local_tz)
    #now = now.replace(minute=0, second=0, microsecond=0)
    proc_data = PROC(data)
    for d in proc_data:
        computer_id = d[0][0]['text']
        try:
            common_id = Xfactor_Common.objects.get(computer_id=computer_id)
        except Exception as e:
            print(computer_id)
            print(e)
            print("미닛틀리 예외발생")
            continue  # 다음 for문으로 넘어감
        defaults = {
            'mem_use': d[1][0]['text'],
            'disk_use': d[2][0]['text'],
            'user_date': now
        }
        computer_id = common_id.computer_id
        xfactor_purchase, created = Xfactor_Purchase.objects.update_or_create(computer_id=computer_id, defaults=defaults)
    return HttpResponse("Data saved successfully!")


def plug_in_security(data):
    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    now = utc_now.astimezone(local_tz)
    #now = now.replace(minute=0, second=0, microsecond=0)
    proc_data = PROC(data)
    for d in proc_data:
        chr_list = []
        chr_ver_list = []
        edg_list = []
        edg_ver_list = []
        fir_list = []
        fir_ver_list = []
        computer_id = d[0][0]['text']
        try:
            common_id = Xfactor_Common.objects.get(computer_id=computer_id)

        except Exception as e:
            print(computer_id)
            print(e)
            print("미닛틀리 예외발생")
            continue  # 다음 for문으로 넘어감
        for c in range(len(d[15])):
            chr_list.append(d[15][c]['text'])
            chr_ver_list.append(d[16][c]['text'])
        for e in range(len(d[17])):
            edg_list.append(d[17][e]['text'])
            edg_ver_list.append(d[18][e]['text'])
        for f in range(len(d[19])):
            fir_list.append(d[19][f]['text'])
            fir_ver_list.append(d[20][f]['text'])
        defaults = {
            'security1': d[1][0]['text'],
            'security1_ver': d[2][0]['text'],
            'security2': d[3][0]['text'],
            'security2_ver': d[4][0]['text'],
            'security3': d[5][0]['text'],
            'security3_ver': d[6][0]['text'],
            'security4': d[7][0]['text'],
            'security4_ver': d[8][0]['text'],
            'security5': d[9][0]['text'],
            'security5_ver': d[10][0]['text'],
            'uuid': d[11][0]['text'],
            'multi_boot': d[12][0]['text'],
            'first_network': d[13][0]['text'],
            'last_boot': d[14][0]['text'],
            'ext_chr': str(chr_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
            'ext_chr_ver': str(chr_ver_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
            'ext_edg': str(edg_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
            'ext_edg_ver': str(edg_ver_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
            'ext_fir': str(fir_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
            'ext_fir_ver': str(fir_ver_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
            'user_date': now
        }
        computer_id = common_id.computer_id
        xfactor_security, created = Xfactor_Security.objects.update_or_create(computer_id=computer_id, defaults=defaults)
        # xfactor_security, created = Xfactor_Security.objects.update_or_create(computer=common_id,  **defaults)
        # xfactor_security = Xfactor_Security.objects.create(computer=common_id, **defaults)
        # xfactor_security.save()
    return HttpResponse("Data saved successfully!")



def plug_in_daily(data):
    try:
        proc_data = PROC(data)
        for d in proc_data:
            #hw_list = []
            sw_list = []
            sw_ver_list = []
            sw_ver_install_list = []
            sw_ver_lastrun_list = []
            hot_list = []
            hotdate_list = []
            chr_list = []
            chr_ver_list = []
            edg_list = []
            edg_ver_list = []
            fir_list = []
            fir_ver_list = []
            # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
            local_tz = pytz.timezone('Asia/Seoul')
            # UTC 시간대를 사용하여 현재 시간을 얻음
            utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
            # 현재 시간대로 시간 변환
            now = utc_now.astimezone(local_tz)
            now = now.replace(minute=0, second=0, microsecond=0)
            #print(now)
            for s in range(len(d[14])):
                sw_list.append(d[14][s]['text'])
                sw_ver_list.append(d[15][s]['text'])
                sw_ver_install_list.append(d[16][s]['text'])
                sw_ver_lastrun_list.append(d[17][s]['text'])
            for i in range(len(d[20])):
                hot_list.append(d[20][i]['text'])
                hotdate_list.append(d[21][i]['text'])
            for c in range(len(d[43])):
                chr_list.append(d[43][c]['text'])
                chr_ver_list.append(d[44][c]['text'])
            for e in range(len(d[45])):
                edg_list.append(d[45][e]['text'])
                edg_ver_list.append(d[46][e]['text'])
            for f in range(len(d[47])):
                fir_list.append(d[47][f]['text'])
                fir_ver_list.append(d[48][f]['text'])
            # xfactor_user = Xfactor_Common()
            # xfactor_user_log = Xfactor_Common_log()
            computer_id = d[0][0]['text']
            defaults = {
                'computer_name': d[1][0]['text'],
                'ip_address': d[2][0]['text'],
                'mac_address': d[3][0]['text'],
                'chassistype': d[4][0]['text'],
                'os_simple': d[5][0]['text'],
                'os_total': d[6][0]['text'].replace('Microsoft ', ''),
                'os_version': d[7][0]['text'],
                'os_build': d[8][0]['text'],
                'hw_cpu' : d[9][0]['text'],
                'hw_ram' : d[10][0]['text'],
                'hw_mb' : d[11][0]['text'],
                'hw_disk' : d[12][0]['text'],
                'hw_gpu' : d[13][0]['text'],
                'sw_list': str(sw_list).replace('"','').replace('!','<br>').replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_ver_list': str(sw_ver_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_install' : str(sw_ver_install_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'sw_lastrun' : str(sw_ver_lastrun_list).replace("!","<br>").replace('\'','').replace('[','').replace(']','').replace(', ',''),
                'first_network' : d[18][0]['text'],
                'last_network' : d[19][0]['text'],
                'hotfix': str(hot_list).replace("''", '').replace("' ", '').replace("'", '').replace(",", "<br>").replace('[', '').replace(']', ''),
                'hotfix_date': str(hotdate_list).replace("''", '').replace("' ", '').replace("'", '').replace(",", "<br>").replace('[', '').replace(']', ''),
                'subnet' : d[22][0]['text'],
                'essential1': d[23][0]['text'],
                'essential2': d[24][0]['text'],
                'essential3': d[25][0]['text'],
                'essential4': d[26][0]['text'],
                'essential5': d[27][0]['text'],
                'mem_use': d[28][0]['text'],
                'disk_use': d[29][0]['text'],
                't_cpu': d[30][0]['text'],
                'security1': d[31][0]['text'],
                'security1_ver': d[32][0]['text'],
                'security2': d[33][0]['text'],
                'security2_ver': d[34][0]['text'],
                'security3': d[35][0]['text'],
                'security3_ver': d[36][0]['text'],
                'security4': d[37][0]['text'],
                'security4_ver': d[38][0]['text'],
                'security5': d[39][0]['text'],
                'security5_ver': d[40][0]['text'],
                'uuid': d[41][0]['text'],
                'multi_boot': d[42][0]['text'],
                'ext_chr': str(chr_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
                'ext_chr_ver': str(chr_ver_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
                'ext_edg': str(edg_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
                'ext_edg_ver': str(edg_ver_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
                'ext_fir': str(fir_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
                'ext_fir_ver': str(fir_ver_list).replace("['', '", '').replace(", '', ", "<br>").replace("''", '').replace("' ", '').replace("'", '').replace(", ", "<br>").replace('[', '').replace(']', ''),
                'logged_name': d[49][0]['text'].replace('NC-KOREA\\',''),
                'user_date': now
            }
            xfactor_common_log = Xfactor_Daily.objects.create(computer_id=computer_id, **defaults)
            xfactor_common_log.save()
    except Exception as e:
        print(d)
        print(e)
    return HttpResponse("Data saved successfully!")

def cache():
    if Xfactor_Common.objects.all() != None:
        xfactor_common_records = Xfactor_Common.objects.all()

        # Xfactor_Common_Cache 업데이트
        for record in xfactor_common_records:
            Xfactor_Common_Cache.objects.create(
                computer_id=record.computer_id,
                computer_name=record.computer_name,
                ip_address=record.ip_address,
                mac_address=record.mac_address,
                chassistype=record.chassistype,
                os_simple=record.os_simple,
                os_total=record.os_total.replace('Microsoft ', ''),
                os_version=record.os_version,
                os_build=record.os_build,
                hw_cpu=record.hw_cpu,
                hw_ram=record.hw_ram,
                hw_mb=record.hw_mb,
                hw_disk=record.hw_disk,
                hw_gpu=record.hw_gpu,
                sw_list=record.sw_list,
                sw_ver_list=record.sw_ver_list,
                sw_install=record.sw_install,
                sw_lastrun=record.sw_lastrun,
                first_network=record.first_network,
                last_network=record.last_network,
                hotfix=record.hotfix,
                hotfix_date=record.hotfix_date,
                subnet=record.subnet,
                memo=record.memo,
                essential1=record.essential1,
                essential2=record.essential2,
                essential3=record.essential3,
                essential4=record.essential4,
                essential5=record.essential5,
                mem_use=record.mem_use,
                disk_use=record.disk_use,
                t_cpu=record.t_cpu,
                logged_name=record.logged_name,
                cache_date=record.user_date,
                user_date=timezone.now()
                # 필요한 모든 필드 추가...
            )