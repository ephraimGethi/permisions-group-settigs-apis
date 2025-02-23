from django.urls import path
from . import api
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('',api.conversations_list,name='api_conversation_list'),
    path('token/',TokenObtainPairView.as_view()),
    path('token/refresh_token/',TokenRefreshView.as_view()),
    path('<uuid:pk>/',api.conversations_detail,name='api_conversations_detail'),
    path('start/<uuid:user_id>/',api.conversation_start,name='api_conversation_start'),path('groups/create/', api.CreateGroupAPIView.as_view(), name='create-group'),
    path('groups/add-user/', api.AddUserToGroupAPIView.as_view(), name='add-user-to-group'),
    path('groups/assign-permission/', api.AssignPermissionToGroupAPIView.as_view(), name='assign-permission-to-group'),
    ]