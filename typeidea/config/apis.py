from rest_framework import viewsets

from .serializers import SideBarSerializer
from .models import SideBar
from rest_framework.response import Response

class SidebarViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super(SidebarViewSet, self).list(request,*args, **kwargs)
        print("90909090")
        print(response.data)
        response.data = {'result': {'data' : response.data}}
        return response

    queryset = SideBar.objects.filter(status=SideBar.STATUS_SHOW)
    serializer_class = SideBarSerializer