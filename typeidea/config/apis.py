from rest_framework import viewsets

from .serializers import SideBarSerializer
from .models import SideBar

class SidebarViewSet(viewsets.ModelViewSet):
    queryset = SideBar.objects.filter(status=SideBar.STATUS_SHOW)
    serializer_class = SideBarSerializer