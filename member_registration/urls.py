from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import MemberViewSet, token_login


router = DefaultRouter()
router.register(r'member', MemberViewSet, basename= 'member')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'member': reverse('member-list', request=request, format=format),
        'login': reverse('login', request=request, format=format),
    })



urlpatterns = [
    path('', api_root, name = 'api-root'),
    path('', include(router.urls)),
    path('login/', token_login, name= 'login')
]