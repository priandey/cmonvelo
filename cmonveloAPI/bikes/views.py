import random
import secrets

from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from geopy.distance import distance as dist
from mail_templated import send_mail

from .models import Bike, Owner, FoundAlert, Trait, ModerationToken
from .serializers import BikeOwnerSerializer, BikePublicSerializer, FoundAlertSerializer, TraitSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['GET',])
def VerifyToken(request):
    if isinstance(request.user, Owner):
        return Response(status=200)
    else:
        return Response(status=401)

@api_view(['POST',])
def AskModeration(request):
    try:
        reason = request.POST['reason']
        message = request.POST['message']
        bike_id = int(request.POST['bike'])
    except KeyError as e:
        raise ValidationError(f'Il manque des paramètres à votre requête : {e}')

    try:
        bike = Bike.objects.get(pk=bike_id)
    except Bike.DoesNotExist:
        raise NotFound("Ce vélo n'existe pas")
    moderation_token = secrets.token_urlsafe()
    ModerationToken.objects.create(token=moderation_token)
    from_email = "noreply@wantedvelo.org"
    send_mail(
        template_name='bikes/email_moderation.html',
        context={'bike': bike,
                 'reason': reason,
                 'message': message,
                 'token': moderation_token
                 },
        from_email=from_email,
        recipient_list=settings.MODERATORS_EMAILS,
        subject='Une modération a été demandée'
    )
    return Response(status=200)

@api_view(['GET',])
def ModerateBike(request, pk, token):
    try:
        moderation_token = ModerationToken.objects.get(token=token)
    except ModerationToken.DoesNotExist:
        return Response(status=403, data="Vous n'avez pas les permissions nécessaires")

    moderation_token.delete()

    try:
        bike = Bike.objects.get(pk=pk)
        bike.delete()
    except Bike.DoesNotExist:
        return Response(status=404, data="Ce vélo n'existe pas (ou plus)")
    return Response(status=202, data="Annonce supprimée")

class RobbedBikesView(generics.ListCreateAPIView):
    """
        url: /
        description: List of robbed bikes. Allow creation of new bikes for authenticated users
        params: {
                {
                    name: "search_type"
                    type/desc: str() "all"/"near"/"owned"
                    required: False
                },
                {
                    name: "lon"
                    type/desc: float() longitude in radians
                    required: False
                },
                {
                    name: "lat"
                    type/desc: float() latitude in radians
                    required: False
                },
            }
        methods:
            GET:
            POST:
    """
    queryset = Bike.objects.filter(robbed=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.query_params.get('search_type', default="all") == "owned":
            return BikeOwnerSerializer
        else:
            return BikePublicSerializer

    def get_queryset(self):
        search_type = self.request.query_params.get('search_type', default="all")

        if search_type == 'all':
            queryset = self.queryset.order_by('-date_of_robbery')

        elif search_type == 'owned':
            try:
                queryset = self.queryset.filter(owner=self.request.user)
            except TypeError:
                raise ValidationError(detail="Invalid authentication Token")

        elif search_type == 'filtered':
            traits = self.request.query_params.get('traits', default='')
            if traits != '':
                traitslist = traits.split(",")
                querysets = []
                for trait in traitslist:
                    byref = self.queryset.filter(reference__iexact=trait)
                    if(byref.exists()):
                        querysets.append(byref)
                    else:
                        querysets.append(self.queryset.filter(traits__in=[trait]))
                initial_queryset = querysets.pop(0)
                queryset = initial_queryset.intersection(*querysets).distinct().order_by('-date_of_robbery')
            else:
                raise ValidationError(detail="""Invalid parameters:
                                                You should specify traits as filter""")

        elif search_type == 'near':
            lon = self.request.query_params.get('lon', default="2.349903")  # Default coords are located in Paris
            lat = self.request.query_params.get('lat', default="48.852969")
            try:
                user_location = (float(lat), float(lon))
                queryset = self.get_by_geolocation(user_location)
            except ValueError:
                raise ValidationError(detail="Invalid Parameters : "
                                             "'lon' should be longitude in radians,"
                                             "'lat' should be latitude in radians")

        else:
            raise ValidationError(detail="""Invalid parameters : 
                                            "search_type" is not correctly filled options are :
                                            - 'all'
                                            - 'near'
                                            - 'owned'
                                            - 'filtered'""")
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_by_geolocation(self, coords):
        weighted_bikes = dict()
        result = []
        for bike in Bike.objects.filter(robbed=True):
            distance = dist((bike.robbed_location['latitude'], bike.robbed_location['longitude']), coords).km
            if distance in weighted_bikes:  # Insuring distance is not set, if so add random cm
                distance += random.uniform(0.00001, 0.00009)
            weighted_bikes[distance] = bike
        choice = sorted(list(weighted_bikes.keys()))
        for key in choice:
            result.append(weighted_bikes[key])

        return result

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        url: /bike/<int:pk>/
            description: Allow operation like reading editing or deleting one bike instance
            methods:
                GET:
                PUT:
                PATCH:
                DELETE:
    """
    queryset = Bike.objects.all()
    lookup_field = "pk"
    permission_classes = [IsOwnerOrReadOnly,]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user == self.get_object().owner:
            return BikeOwnerSerializer
        else:
            return BikePublicSerializer


class FoundBikeView(generics.CreateAPIView):
    """
        url: bike/<int:pk>/found/
            description: create a found alert linked to a robbed bike
            methods:
                POST:
                {
                    message: str(),
                    coords:
                    {
                        lon: float(),
                        lat: float()
                    }
                }
    """
    queryset = FoundAlert.objects.all()
    serializer_class = FoundAlertSerializer

    def perform_create(self, serializer):
        my_alert = serializer.save(bike=Bike.objects.get(pk=self.kwargs['pk']))
        # TODO : Email sending should be async
        from_email = "noreply@wantedvelo.org"
        send_mail(
            'bikes/email_alert.html',
            {'alert': my_alert},
            from_email,
            [my_alert.bike.owner.email],
            subject=f'Votre vélo "{my_alert.bike.reference}" a été repéré !'
        )


class TraitsView(generics.ListCreateAPIView):
    """
        url: /traits/
            description: List of matching traits
            params: {
                {
                    name: "qs"
                    type: str()
                    required: True
                }
            }
            methods:
                GET:
                POST:

    """
    model = Trait
    queryset = Trait.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = TraitSerializer

    def perform_create(self, serializer):
        serializer.save(name=serializer.validated_data['name'].lower().capitalize())

    def get_queryset(self):
        query_string = self.request.query_params.get("qs", default="")
        if query_string == "":
            return self.model.objects.none()
        return self.queryset.filter(name__istartswith=query_string)
