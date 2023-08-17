from django.utils import timezone
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# import django
# django.setup()
from ..models import *
from django.db.models import Count, Q

import time
from datetime import datetime, timedelta



#구분데이터 통계
def chassis_type() :
    users = XFactor_User.objects.exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('chasisstype').annotate(count=Count('chasisstype'))
    for user_data in users:
        classification = 'chassis_type'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['chasisstype']
        item_count = user_data['count']
        daily_statistics = Daily_Statistics(
            classification=classification,
            item=item,
            item_count=item_count,
        )
        daily_statistics.save()

def os_type() :
    users = XFactor_User.objects.exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('os_simple').annotate(count=Count('os_simple'))
    for user_data in users:
        classification = 'os_simple'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_simple']
        item_count = user_data['count']
        daily_statistics = Daily_Statistics(
            classification=classification,
            item=item,
            item_count=item_count,
        )
        daily_statistics.save()

def win_ver() :
    users = XFactor_User.objects.filter(Q(os_simple='Windows')).exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed').values('os_total').annotate(count=Count('os_total'))
    for user_data in users:
        classification = 'win_os_total'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = user_data['os_total']
        item_count = user_data['count']
        daily_statistics = Daily_Statistics(
            classification=classification,
            item=item,
            item_count=item_count,
        )
        daily_statistics.save()
