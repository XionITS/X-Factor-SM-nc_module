import logging

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
logger = logging.getLogger()
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
            chr_list = []
            chr_ver_list = []
            edg_list = []
            edg_ver_list = []
            fir_list = []
            fir_ver_list = []

            logged_name_id = d[49][0]['text'].replace('NC-KOREA\\','')
            try:
                logged_name_id = Xfactor_ncdb.objects.get(userId=logged_name_id)
            except Exception as e:
                custom_object = Xfactor_ncdb()
                custom_object.userId = logged_name_id
                custom_object.save()
                logged_name_id = Xfactor_ncdb.objects.get(userId=logged_name_id)

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
                'logged_name_id': logged_name_id,
                'user_date': now
            }
            xfactor_common, created = Xfactor_Common.objects.update_or_create(computer_id=computer_id, defaults=defaults)
            # xfactor_common.save()
    except Exception as e:
        logger.warning('정시 미닛틀리 error' + str(e))
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

            logged_name_id = d[49][0]['text'].replace('NC-KOREA\\','')
            try:
                logged_name_id = Xfactor_ncdb.objects.get(userId=logged_name_id)
            except Exception as e:
                #logged_name_id = d[49][0]['text'].replace('NC-KOREA\\', '')
                logged_name_id = None

            # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
            local_tz = pytz.timezone('Asia/Seoul')
            # UTC 시간대를 사용하여 현재 시간을 얻음
            utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
            # 현재 시간대로 시간 변환
            now = utc_now.astimezone(local_tz)
            now = now.replace(minute=10, second=0, microsecond=0)
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
                'logged_name_id': logged_name_id,
                'user_date': now
            }
            xfactor_common_log = Xfactor_Daily.objects.create(computer_id=computer_id, **defaults)
            xfactor_common_log.save()
    except Exception as e:
        logger.warning('정시 데일리 error' + str(e))
        print(d)
        print(e)
    return HttpResponse("Data saved successfully!")

def cache():
    if Xfactor_Common.objects.exists():
        common_objects = Xfactor_Common.objects.all()

        for common in common_objects:
            try:
                # Xfactor_Common 객체와 동일한 필드 값을 가진 Xfactor_Common_Cache 객체를 생성합니다.
                cache = Xfactor_Common_Cache(
                    computer_id=common.computer_id,
                    computer_name=common.computer_name,
                    ip_address=common.ip_address,
                    mac_address=common.mac_address,
                    chassistype=common.chassistype,
                    os_simple=common.os_simple,
                    os_total=common.os_total,
                    os_version=common.os_version,
                    os_build=common.os_build,
                    hw_cpu=common.hw_cpu,
                    hw_ram=common.hw_ram,
                    hw_mb=common.hw_mb,
                    hw_disk=common.hw_disk,
                    hw_gpu=common.hw_gpu,
                    sw_list=common.sw_list,
                    sw_ver_list=common.sw_ver_list,
                    sw_install=common.sw_install,
                    sw_lastrun=common.sw_lastrun,
                    first_network=common.first_network,
                    last_network=common.last_network,
                    hotfix=common.hotfix,
                    hotfix_date=common.hotfix_date,
                    subnet=common.subnet,
                    memo=common.memo,
                    essential1=common.essential1,
                    essential2=common.essential2,
                    essential3=common.essential3,
                    essential4=common.essential4,
                    essential5=common.essential5,
                    mem_use=common.mem_use,
                    disk_use=common.disk_use,
                    t_cpu=common.t_cpu,
                    security1=common.security1,
                    security1_ver=common.security1_ver,
                    security2=common.security2,
                    security2_ver=common.security2_ver,
                    security3=common.security3,
                    security3_ver=common.security3_ver,
                    security4=common.security4,
                    security4_ver=common.security4_ver,
                    security5=common.security5,
                    security5_ver=common.security5_ver,
                    uuid=common.uuid,
                    multi_boot=common.multi_boot,
                    ext_chr=common.ext_chr,
                    ext_chr_ver=common.ext_chr_ver,
                    ext_edg=common.ext_edg,
                    ext_edg_ver=common.ext_edg_ver,
                    ext_fir=common.ext_fir,
                    ext_fir_ver=common.ext_fir_ver,
                    logged_name_id=common.logged_name_id,
                    cache_date=common.user_date,
                    user_date=timezone.now()
                )
                # Xfactor_Common_Cache 객체를 데이터베이스에 저장합니다.
                cache.save()
            except Exception as e:
                logger.warning('정시 캐시 error' + str(e))
                # Xfactor_Common 객체가 존재하지 않는 경우, 빈 필드를 가진 Xfactor_Common_Cache 객체를 생성합니다.
                #cache = Xfactor_Common_Cache()
                #cache.save()
                continue
    print("cache success")