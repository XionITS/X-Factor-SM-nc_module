from django.db import models, transaction
#
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


class Xfactor_ncdb(models.Model):
    companyCode = models.CharField(max_length=100, null=True)
    userName = models.CharField(max_length=100, null=True)
    userNameEn = models.CharField(max_length=100, null=True)
    userId = models.CharField(primary_key=True, max_length=100)
    email = models.CharField(max_length=100, null=True)
    empNo = models.CharField(max_length=100, null=True)
    joinDate = models.CharField(max_length=100, null=True)
    retireDate = models.CharField(max_length=100, null=True)
    deptCode = models.CharField(max_length=100, null=True)
    deptName = models.CharField(max_length=100, null=True)
    managerUserName = models.CharField(max_length=100, null=True)
    managerUserId = models.CharField(max_length=100, null=True)
    managerEmpNo = models.CharField(max_length=100, null=True)

class Xfactor_Common(models.Model):
    computer_id = models.CharField(max_length=100, primary_key=True)
    computer_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    chassistype = models.CharField(max_length=100)
    os_simple = models.CharField(max_length=100)
    os_total = models.CharField(max_length=100)
    os_version = models.CharField(max_length=500)
    os_build = models.CharField(max_length=500)
    hw_cpu = models.CharField(max_length=500)
    hw_ram = models.CharField(max_length=500)
    hw_mb = models.CharField(max_length=500)
    hw_disk = models.CharField(max_length=500)
    hw_gpu = models.CharField(max_length=500)
    sw_list = models.TextField()
    sw_ver_list = models.TextField()
    sw_install = models.TextField(null=True)
    sw_lastrun = models.TextField(null=True)
    first_network = models.TextField(null=True)
    last_network = models.TextField(null=True)
    hotfix = models.TextField(null=True)
    hotfix_date = models.TextField(null=True)
    subnet = models.TextField(null=True)
    memo = models.TextField(null=True)
    essential1 = models.CharField(max_length=100, null=True)
    essential2 = models.CharField(max_length=100, null=True)
    essential3 = models.CharField(max_length=100, null=True)
    essential4 = models.CharField(max_length=100, null=True)
    essential5 = models.CharField(max_length=100, null=True)
    mem_use = models.CharField(max_length=100, null=True)
    disk_use = models.CharField(max_length=100, null=True)
    t_cpu = models.CharField(max_length=100, null=True)
    logged_name_id = models.ForeignKey(Xfactor_ncdb, on_delete=models.SET_NULL, null=True, db_column="logged_name")
    user_date = models.DateTimeField(auto_now_add=True)

class Xfactor_Daily(models.Model):
    computer_id = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    chassistype = models.CharField(max_length=100)
    os_simple = models.CharField(max_length=100)
    os_total = models.CharField(max_length=100)
    os_version = models.CharField(max_length=500)
    os_build = models.CharField(max_length=500)
    hw_cpu = models.CharField(max_length=500)
    hw_ram = models.CharField(max_length=500)
    hw_mb = models.CharField(max_length=500)
    hw_disk = models.CharField(max_length=500)
    hw_gpu = models.CharField(max_length=500)
    sw_list = models.TextField()
    sw_ver_list = models.TextField()
    sw_install = models.TextField(null=True)
    sw_lastrun = models.TextField(null=True)
    first_network = models.TextField(null=True)
    last_network = models.TextField(null=True)
    hotfix = models.TextField(null=True)
    hotfix_date = models.TextField(null=True)
    subnet = models.CharField(max_length=100)
    memo = models.TextField(null=True)
    essential1 = models.CharField(max_length=100)
    essential2 = models.CharField(max_length=100)
    essential3 = models.CharField(max_length=100)
    essential4 = models.CharField(max_length=100)
    essential5 = models.CharField(max_length=100)
    mem_use = models.CharField(max_length=100)
    disk_use = models.CharField(max_length=100)
    t_cpu = models.CharField(max_length=100)
    security1 = models.CharField(max_length=100)
    security2 = models.CharField(max_length=100)
    security3 = models.CharField(max_length=100)
    security4 = models.CharField(max_length=100)
    security5 = models.CharField(max_length=100)
    security1_ver = models.CharField(max_length=100)
    security2_ver = models.CharField(max_length=100)
    security3_ver = models.CharField(max_length=100)
    security4_ver = models.CharField(max_length=100)
    security5_ver = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)
    multi_boot = models.CharField(max_length=100)
    ext_chr = models.TextField()
    ext_chr_ver = models.TextField()
    ext_edg = models.TextField()
    ext_edg_ver = models.TextField()
    ext_fir = models.TextField()
    ext_fir_ver = models.TextField()
    logged_name_id = models.ForeignKey(Xfactor_ncdb, on_delete=models.SET_NULL, null=True, db_column="logged_name")
    user_date = models.DateTimeField()


class Xfactor_Purchase(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    mem_use = models.TextField()
    disk_use = models.TextField()
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Security(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    security1 = models.CharField(max_length=100)
    security2 = models.CharField(max_length=100)
    security3 = models.CharField(max_length=100)
    security4 = models.CharField(max_length=100)
    security5 = models.CharField(max_length=100)
    security1_ver = models.CharField(max_length=100)
    security2_ver = models.CharField(max_length=100)
    security3_ver = models.CharField(max_length=100)
    security4_ver = models.CharField(max_length=100)
    security5_ver = models.CharField(max_length=100)
    uuid = models.CharField(max_length=500)
    multi_boot = models.TextField()
    first_network = models.TextField()
    last_boot = models.TextField()
    ext_chr = models.TextField()
    ext_chr_ver = models.TextField()
    ext_edg = models.TextField()
    ext_edg_ver = models.TextField()
    ext_fir = models.TextField()
    ext_fir_ver = models.TextField()
    user_date = models.DateTimeField(auto_now_add=True)



class Xfactor_Nano(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50, null=True)
    user_email = models.EmailField(null=True)
    user_dep = models.CharField(max_length=50, null=True)
    domain_id = models.CharField(max_length=50, null=True)
    open_id = models.CharField(max_length=50, null=True)
    xfactor_id = models.CharField(max_length=50, null=True)
    depno = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=100, null=True)

class Xfactor_Xuser(models.Model):
    x_id = models.CharField(max_length=500, primary_key=True)
    x_pw = models.CharField(max_length=500, null=True)
    x_name = models.CharField(max_length=50, null=True)
    x_email = models.CharField(max_length=500, null=True)
    x_auth = models.CharField(max_length=500, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

class Xfactor_Xuser_Group(models.Model):
    xgroup_name = models.CharField(max_length=500)
    xgroup_note = models.TextField(null=True)
    xuser_id_list = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

class Xfactor_Auth(models.Model):
    auth_id = models.CharField(max_length=500, primary_key=True)
    auth_name = models.CharField(max_length=500)
    auth_url = models.CharField(max_length=500)
    auth_num = models.IntegerField()


class Xfactor_Xuser_Auth(models.Model):
    auth_use = models.CharField(max_length=500)
    xfactor_xuser = models.ForeignKey(Xfactor_Xuser, on_delete=models.CASCADE, related_name='xuser', to_field='x_id')
    xfactor_auth = models.ForeignKey(Xfactor_Auth, on_delete=models.CASCADE, related_name='auth', to_field='auth_id')

class Xfactor_Xgroup_Auth(models.Model):
    auth_use = models.CharField(max_length=500)
    xfactor_xgroup = models.TextField(null=True)
    xgroup = models.ForeignKey(Xfactor_Xuser_Group, on_delete=models.CASCADE, related_name='xgroup', to_field='id')
    xfactor_auth = models.ForeignKey(Xfactor_Auth, on_delete=models.CASCADE, related_name='group_auth', to_field='auth_id')


class Daily_Statistics(models.Model):
    daily_statistics_num = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    classification = models.CharField(max_length=500)
    item = models.TextField()
    item_count = models.IntegerField()
    statistics_collection_date = models.DateTimeField(auto_now=True)


class Daily_Statistics_log(models.Model):
    daily_statistics_num = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    classification = models.CharField(max_length=500)
    item = models.TextField()
    item_count = models.IntegerField()
    statistics_collection_date = models.DateTimeField(auto_now=True)


class Xfactor_Group(models.Model):
    group_id = models.CharField(max_length=500, primary_key=True)
    group_name = models.CharField(max_length=500)
    group_note = models.TextField(null=True)
    computer_id_list = models.TextField(null=True)
    computer_name_list = models.TextField(null=True)


class Xfactor_Deploy(models.Model):
    deploy_id = models.CharField(max_length=500, primary_key=True)
    group_id = models.ForeignKey(Xfactor_Group, on_delete=models.CASCADE)
    deploy_name = models.CharField(max_length=500)


class Xfactor_Report(models.Model):
    report_num = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    classification = models.CharField(max_length=500)
    item = models.TextField()
    item_count = models.IntegerField()
    report_collection_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Log(models.Model):
    log_func = models.CharField(max_length=100)
    log_item = models.CharField(max_length=100)
    log_result = models.CharField(max_length=100)
    log_user = models.CharField(max_length=100)
    log_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Common_Cache(models.Model):
    computer_id = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    chassistype = models.CharField(max_length=100)
    os_simple = models.CharField(max_length=100)
    os_total = models.CharField(max_length=100)
    os_version = models.CharField(max_length=500)
    os_build = models.CharField(max_length=500)
    hw_cpu = models.CharField(max_length=500)
    hw_ram = models.CharField(max_length=500)
    hw_mb = models.CharField(max_length=500)
    hw_disk = models.CharField(max_length=500)
    hw_gpu = models.CharField(max_length=500)
    sw_list = models.TextField()
    sw_ver_list = models.TextField()
    sw_install = models.TextField(null=True)
    sw_lastrun = models.TextField(null=True)
    first_network = models.TextField(null=True)
    last_network = models.TextField(null=True)
    hotfix = models.TextField(null=True)
    hotfix_date = models.TextField(null=True)
    subnet = models.TextField(null=True)
    memo = models.TextField(null=True)
    essential1 = models.CharField(max_length=100, null=True)
    essential2 = models.CharField(max_length=100, null=True)
    essential3 = models.CharField(max_length=100, null=True)
    essential4 = models.CharField(max_length=100, null=True)
    essential5 = models.CharField(max_length=100, null=True)
    mem_use = models.CharField(max_length=100, null=True)
    disk_use = models.CharField(max_length=100, null=True)
    t_cpu = models.CharField(max_length=100, null=True)
    logged_name_id = models.ForeignKey(Xfactor_ncdb, on_delete=models.SET_NULL, null=True, db_column="logged_name")
    cache_date = models.DateTimeField(null=True)
    user_date = models.DateTimeField(auto_now_add=True)