
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# import django
# django.setup()
from ..models import *
from django.db.models import Count, Q

import time
from datetime import datetime, timedelta


#구분데이터 통계
def Minutely_statistics() :
    #chassis_type 섀시타입
    user = Xfactor_Common.objects.all()
    users = user.exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('chassistype').annotate(count=Count('chassistype'))
    for user_data in users:
        classification = 'chassis_type'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['chassistype']
        item_count = user_data['count']
        daily_statistics, created = Daily_Statistics.objects.get_or_create(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics.save()

    #os_type OS종류
    users = user.exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('os_simple').annotate(count=Count('os_simple'))
    for user_data in users:
        classification = 'os_simple'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_simple']
        item_count = user_data['count']
        daily_statistics, created = Daily_Statistics.objects.get_or_create(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics.save()

    #win_ver 윈도우버전
    users = user.filter(Q(os_simple='Windows')).exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('os_total').annotate(count=Count('os_total'))
    for user_data in users:
        classification = 'win_os_total'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_total']
        item_count = user_data['count']
        daily_statistics, created = Daily_Statistics.objects.get_or_create(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics.save()
    print("Minutely Statistics Success")

def Daily() :
    #print("daily start")
    #chassis_type 섀시타입
    user = Xfactor_Common_log.objects.all()
    users = user.exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('chassistype').annotate(count=Count('chassistype'))
    for user_data in users:
        classification = 'chassis_type'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['chassistype']
        item_count = user_data['count']
        daily_statistics_log = Daily_Statistics_log(
            classification=classification,
            item=item,
            item_count=item_count
        )
        daily_statistics_log.save()

    #os_type OS종류
    users = user.exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('os_simple').annotate(count=Count('os_simple'))
    for user_data in users:
        classification = 'os_simple'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_simple']
        item_count = user_data['count']
        daily_statistics_log = Daily_Statistics_log(
            classification=classification,
            item=item,
            item_count=item_count
        )
        daily_statistics_log.save()

    #win_ver 윈도우버전
    users = user.filter(Q(os_simple='Windows')).exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('os_total').annotate(count=Count('os_total'))
    for user_data in users:
        classification = 'win_os_total'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_total']
        item_count = user_data['count']
        daily_statistics_log= Daily_Statistics_log(
            classification=classification,
            item=item,
            item_count=item_count
        )
        daily_statistics_log.save()
    print("daily Statistics Success")