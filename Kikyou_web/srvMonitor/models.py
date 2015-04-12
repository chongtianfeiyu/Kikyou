#coding=utf-8
from django.db import models

# Create your models here.
class grpInfo(models.Model):
	grp_id = models.IntegerField(verbose_name='项目组ID')
	grp_name = models.CharField(max_length=30,verbose_name='项目组名')
	grp_status = models.SmallIntegerField(verbose_name='项目状态')
	app_id = models.CharField(max_length=20,verbose_name='APP ID',blank=True)
	admin_email = models.EmailField(blank=True,null=True,verbose_name='管理员Email')
	
	def __unicode__(self):
		return self.grp_name

class srvInfo(models.Model):
	grp_id = models.ForeignKey(grpInfo)
	srv_name = models.CharField(max_length=30,verbose_name='服务器名')
	ip_vlan = models.IPAddressField(verbose_name='内网ip')
	ip_wlan = models.IPAddressField(null=True,blank=True,verbose_name='外网ip')
	core_num = models.IntegerField(verbose_name='CPU颗数')
	mem_size = models.FloatField(null=True,default=0.0,verbose_name='内存大小')
	disk_size = models.IntegerField(verbose_name='大磁盘容量')
	os_version = models.CharField(max_length=30,verbose_name='操作系统版本')
	prize = models.FloatField(null=True,default=0.0,blank=True,verbose_name='价格(元/天)')
	purchase_date = models.DateTimeField(verbose_name='订购日期')
	refund_date = models.DateTimeField(blank=True,null=True,verbose_name='退订日期')
	
	def __unicode__(self):
		return u'%s-%s' % (self.grp_id,self.srv_name)

class srvStatus(models.Model):
	ip_vlan = models.IPAddressField(verbose_name='ip地址',null=False)
	cpu_load5 = models.FloatField(default=0.0)
	cpu_load10 = models.FloatField(default=0.0)
	cpu_load15 = models.FloatField(default=0.0)
	mem_used = models.FloatField(default=0.0)
	tcp_estab = models.IntegerField()
	eth_in = models.IntegerField()
	eth_out = models.IntegerField()
	disk_used_root = models.SmallIntegerField()
	disk_used_data = models.SmallIntegerField()
	inode_used_root = models.SmallIntegerField()
	inode_used_data = models.SmallIntegerField()
	alert_level=models.IntegerField(verbose_name='报警级别',default=0)
	srv_status=models.IntegerField(verbose_name='服务器状态',default=0)
	ts = models.DateTimeField()
	
	def __unicode__(self):
		return self.ip_vlan
	
class tmpStatus(models.Model):
	ipaddr = models.IPAddressField(primary_key=True)
	cpu_load5 = models.FloatField(default=0.0)
	cpu_load10 = models.FloatField(default=0.0)
	cpu_load15 = models.FloatField(default=0.0)
	mem_used = models.FloatField(default=0.0)
	tcp_estab = models.IntegerField()
	eth_in = models.IntegerField()
	eth_out = models.IntegerField()
	disk_used_root = models.SmallIntegerField()
	disk_used_data = models.SmallIntegerField()
	inode_used_root = models.SmallIntegerField()
	inode_used_data = models.SmallIntegerField()
	alert_level=models.IntegerField(verbose_name='报警级别',default=0)
	srv_status=models.IntegerField(verbose_name='服务器状态',default=0)
	ts = models.DateTimeField()	
	