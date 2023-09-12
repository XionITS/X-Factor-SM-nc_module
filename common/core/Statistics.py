
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# import django
# django.setup()
from ..models import *
from django.db.models import Count, Q
import pytz
import time
from datetime import datetime, timedelta


#구분데이터 통계
def Minutely_statistics() :
    #chassis_type 섀시타입
    Daily_Statistics.objects.all().delete()

    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    time = now - timedelta(minutes=7)
    user = Xfactor_Common.objects.filter(user_date__gte=time)
    service = Xfactor_Service.objects.filter(user_date__gte=time)
    #user = Xfactor_Common.objects.exclude(computer_id='unconfirmed').filter(user_date__gte=time)
    users = user.values('chassistype').annotate(count=Count('chassistype'))
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
    users = user.values('os_simple').annotate(count=Count('os_simple'))
    #print(users)
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
    users = user.filter(Q(os_simple='Windows')).values('os_total').annotate(count=Count('os_total'))
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

    #subnet 대역별
    users = user.values('subnet').annotate(count=Count('subnet'))
    for user_data in users:
        classification = 'subnet'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['subnet']
        item_count = user_data['count']
        daily_statistics, created = Daily_Statistics.objects.get_or_create(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics.save()

    # cpu 사용량
    services = service.values('t_cpu').annotate(count=Count('t_cpu'))
    for service_data in services:
        classification = 't_cpu'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = service_data['t_cpu']
        item_count = service_data['count']
        daily_statistics, created = Daily_Statistics.objects.get_or_create(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics.save()

    # os버전별 자산 현황
    user = Xfactor_Common.objects.filter(user_date__gte=time)
    users = user.filter(Q(os_simple='Windows')).values('os_total', 'os_build').annotate(count=Count('os_total')).order_by('-count')[:6]
    print(users)
    for user_data in users:
        classification = 'win_os_build'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        if user_data['os_total'] == 'unconfirmed':
            continue
        item = user_data['os_total'].split('Microsoft ')[1] + ' ' + user_data['os_build']
        item_count = user_data['count']
        daily_statistics, created = Daily_Statistics.objects.get_or_create(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics.save()

    # 업데이트 필요 통계
    users = user.filter(Q(os_simple='Windows'), os_build__gte='19044').values('os_total', 'os_build').annotate(count=Count('os_total'))
    print(users)
    classification = 'os_version_up'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    item = 'new'
    item_count = sum(item['count'] for item in users)
    daily_statistics, created = Daily_Statistics.objects.get_or_create(
        classification=classification,
        item=item,
        defaults={'item_count': item_count}
    )
    daily_statistics.save()
    # 업데이트 필요 통계
    users = user.filter(Q(os_simple='Windows'), os_build__lt='19044').values('os_total', 'os_build').annotate(count=Count('os_total'))
    print(users)
    classification = 'os_version_up'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    item = 'old'
    item_count = sum(item['count'] for item in users)
    daily_statistics, created = Daily_Statistics.objects.get_or_create(
        classification=classification,
        item=item,
        defaults={'item_count': item_count}
    )
    daily_statistics.save()

    print("Minutely Statistics Success")



def Daily_statistics() :
    #print("daily start")
    #chassis_type 섀시타입
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = start_of_today + timedelta(days=1)

    #user = Xfactor_Daily.objects.filter(user_date__date=now.date())
    user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
    service = Xfactor_Service.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
    #user = Xfactor_Common_log.objects.exclude(computer_id='unconfirmed').filter(user_date__date=now.date())
    users = user.values('chassistype').annotate(count=Count('chassistype'))
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
    users = user.values('os_simple').annotate(count=Count('os_simple'))
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
    users = user.filter(Q(os_simple='Windows')).values('os_total', 'os_build').annotate(count=Count('os_total'))
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

    #subnet 대역별
    users = user.values('subnet').annotate(count=Count('subnet'))
    for user_data in users:
        classification = 'subnet'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['subnet']
        item_count = user_data['count']
        daily_statistics_log = Daily_Statistics_log(
            classification=classification,
            item=item,
            item_count=item_count
        )
        daily_statistics_log.save()

    # cpu 사용량
    services = service.values('t_cpu').annotate(count=Count('t_cpu'))
    for service_data in services:
        classification = 't_cpu'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = service_data['t_cpu']
        item_count = service_data['count']
        daily_statistics_log = Daily_Statistics_log(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics_log.save()

    # os버전별 자산 현황
    users = user.filter(Q(os_simple='Windows')).values('os_total', 'os_build').annotate(count=Count('os_total')).order_by('-count')[:6]
    for user_data in users:
        classification = 'win_os_build'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_total'].split('Microsoft ')[1] + ' ' + user_data['os_build']
        item_count = user_data['count']
        daily_statistics_log = Daily_Statistics_log(
            classification=classification,
            item=item,
            defaults={'item_count': item_count}
        )
        daily_statistics_log.save()

    # # 업데이트 필요 통계
    # users = user.filter(Q(os_simple='Windows'), os_build__gte='19044').values('os_total', 'os_build').annotate(count=Count('os_total'))
    # classification = 'os_version_up'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    # item = 'new'
    # item_count = sum(item['count'] for item in users)
    # daily_statistics_log = Daily_Statistics_log(
    #     classification=classification,
    #     item=item,
    #     defaults={'item_count': item_count}
    # )
    # daily_statistics_log.save()
    # # 업데이트 필요 통계
    # users = user.filter(Q(os_simple='Windows'), os_build__lt='19044').values('os_total', 'os_build').annotate(count=Count('os_total'))
    # classification = 'os_version_up'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    # item = 'old'
    # item_count = sum(item['count'] for item in users)
    # daily_statistics_log = Daily_Statistics_log(
    #     classification=classification,
    #     item=item,
    #     defaults={'item_count': item_count}
    # )
    # daily_statistics_log.save()

    print("daily Statistics Success")