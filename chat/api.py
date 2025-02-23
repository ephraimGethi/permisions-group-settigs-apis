from rest_framework.decorators import api_view,permission_classes,renderer_classes,authentication_classes
from django.http import JsonResponse
from .serializers import ConversationListSerializer,ConversationDetailSerializer,ConversationMessageSerializer
from .models import Conversation,ConversationMessage
from django.contrib.auth.models import User


from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import Group, User, Permission

class CreateGroupAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]  

    def post(self, request):
        group_name = request.data.get('name')
        if not group_name:
            return Response({'error': 'Group name is required'}, status=status.HTTP_400_BAD_REQUEST)

        group, created = Group.objects.get_or_create(name=group_name)
        message = 'Group created' if created else 'Group already exists'
        return Response({'message': message, 'group': group_name}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class AddUserToGroupAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        username = request.data.get('username')
        group_name = request.data.get('group_name')

        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            return Response({'message': f'User {username} added to group {group_name}'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

class AssignPermissionToGroupAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        group_name = request.data.get('group_name')
        permission_codename = request.data.get('permission_codename')

        try:
            group = Group.objects.get(name=group_name)
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)
            return Response({'message': f'Permission {permission_codename} added to group {group_name}'}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        except Permission.DoesNotExist:
            return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)


class AssignPermissionToGroupAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        group_name = request.data.get('group_name')
        app_label = request.data.get('app_label')  # e.g., "chat"
        model_name = request.data.get('model_name')  # e.g., "conversation"
        permission_type = request.data.get('permission_type')  # e.g., "add"

        if not all([group_name, app_label, model_name, permission_type]):
            return Response({'error': 'All fields (group_name, app_label, model_name, permission_type) are required'}, status=status.HTTP_400_BAD_REQUEST)

        permission_codename = f"{permission_type}_{model_name}"  # Example: "add_conversation"

        try:
            group = Group.objects.get(name=group_name)
            permission = Permission.objects.get(content_type__app_label=app_label, codename=permission_codename)
            group.permissions.add(permission)
            return Response({'message': f'Permission {permission_codename} added to group {group_name}'}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        except Permission.DoesNotExist:
            return Response({'error': f'Permission {permission_codename} not found in {app_label} app'}, status=status.HTTP_404_NOT_FOUND)

class AssignMultiplePermissionsToGroupAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """
        Assign multiple permissions to a group.

        Expected JSON:
        {
            "group_name": "Editors",
            "permissions": [
                {"app_label": "chat", "model_name": "conversation", "permission_type": "add"},
                {"app_label": "chat", "model_name": "conversation", "permission_type": "change"},
                {"app_label": "chat", "model_name": "conversation", "permission_type": "delete"},
                {"app_label": "auth", "model_name": "user", "permission_type": "add"},
                {"app_label": "auth", "model_name": "user", "permission_type": "change"},
                {"app_label": "auth", "model_name": "user", "permission_type": "delete"}
            ]
        }
        """
        group_name = request.data.get('group_name')
        permissions_list = request.data.get('permissions')

        if not group_name or not permissions_list:
            return Response({'error': 'Both "group_name" and "permissions" fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        assigned_permissions = []
        not_found_permissions = []

        for perm in permissions_list:
            app_label = perm.get("app_label")
            model_name = perm.get("model_name")
            permission_type = perm.get("permission_type")

            if not app_label or not model_name or not permission_type:
                not_found_permissions.append(perm)
                continue

            permission_codename = f"{permission_type}_{model_name}"  # Example: "add_conversation"

            try:
                permission = Permission.objects.get(content_type__app_label=app_label, codename=permission_codename)
                group.permissions.add(permission)
                assigned_permissions.append(permission_codename)
            except Permission.DoesNotExist:
                not_found_permissions.append(permission_codename)

        return Response({
            'message': 'Permission assignment completed',
            'assigned_permissions': assigned_permissions,
            'not_found_permissions': not_found_permissions
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def conversations_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(),many = True)
    return JsonResponse(serializer.data,safe=False)


@api_view(['GET'])
def conversations_detail(request,pk):

    conversation = request.user.conversations.get(pk=pk)
    conversation_serializer = ConversationDetailSerializer(conversation,many = False)
    messages_serializer = ConversationMessageSerializer(conversation.messages.all(),many = True)
    return JsonResponse({
        'conversation':conversation_serializer.data,
        'messages':messages_serializer.data

    },safe=False)


@api_view(['GET'])
def conversation_start(request,user_id):
    conversations = Conversation.objects.filter(users__in = [user_id]).filter(users__in=[request.user.id])

    if conversations.count() > 0:
        conversation = conversations.first()
        return JsonResponse(
            {
                'success':'already in a conversation','conversation_id':conversation.id
            }
        )
    else:
        user = User.objects.get(pk = user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(user)
        conversation.users.add(request.user)
        
        return JsonResponse(
            {
                'success':'conversation created','conversation_id':conversation.id
            }
        )

