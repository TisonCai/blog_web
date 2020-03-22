from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = 'LetCode'
    site_title = 'LetCode 管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')