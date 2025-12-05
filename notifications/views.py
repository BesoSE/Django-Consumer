from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from notifications.models.user import User
from rest_framework.generics import GenericAPIView

from notifications.serializers import UserSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserListView(GenericAPIView):
    """
    Handles requests for retrieving all users.
    """
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(GenericAPIView):
    """
    Handles requests for retrieving a single user by ID.
    """
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            user = User.objects.last()
        else:
            user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)

        return Response(serializer.data)
