from django.contrib import admin
from srvMonitor.models import *


class GrpInfoAdmin(admin.ModelAdmin):
	list_display = ('grp_id','grp_name','grp_status','app_id','admin_email')

class SrvInfoAdmin(admin.ModelAdmin):
	list_display = ('grp_id','srv_name','ip_vlan','ip_wlan','core_num','mem_size','disk_size','os_version','purchase_date','refund_date')
	search_fields=('srv_name','ip_vlan','ip_wlan')
	# date_hierarchy = 'purchase_date'
	ordering=('-purchase_date',)
	fields=('grp_id','srv_name','ip_vlan','ip_wlan','core_num','mem_size','disk_size','os_version','purchase_date')
	
class SrvStatusAdmin(admin.ModelAdmin):
	list_display = ('ip_vlan','cpu_load5','cpu_load10','cpu_load15','mem_used','tcp_estab','eth_in','eth_out','disk_used_root','disk_used_data','inode_used_root','inode_used_data','ts')
	# list_filter=('cpu_load5','cpu_load10','cpu_load15','eth_in','eth_out','disk_used_root','disk_used_data','inode_used_root','inode_used_data',)
	
admin.site.register(grpInfo,GrpInfoAdmin)
admin.site.register(srvInfo,SrvInfoAdmin)
admin.site.register(srvStatus,SrvStatusAdmin)
