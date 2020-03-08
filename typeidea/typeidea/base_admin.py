from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    '''
    1. 补充保存model时的owner字段
    2. 针对数据查询过滤当前用户的数据
    '''
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request,obj,form,change)