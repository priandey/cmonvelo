from .models import Owner, Bike
from .serializers import OwnerSerializer, BikeOwnerSerializer
from .permissions import IsUser, isOwner

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import authentication, permissions


class UserPannelView(generics.RetrieveUpdateDestroyAPIView):
    '''
        View to interact with the user model
        User need to be authenticated
    '''
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication,]
    serializer_class = OwnerSerializer

    def get_object(self):
        user = get_object_or_404(Owner, pk=self.request.user.pk)
        return user


class BikeListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BikeOwnerSerializer

    def get_queryset(self):
        user = self.request.user
        bikes = Bike.objects.filter(owner=user)
        return bikes

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BikeUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated & isOwner,)
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BikeOwnerSerializer

    def get_object(self):
        bike = get_object_or_404(Bike, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, bike)
        return bike
