import random
from bikeowner.models import Bike
from .models import FoundAlert
from .serializers import BikePublicSerializer, FoundAlertSerializer
from geopy.distance import distance as dist
from rest_framework import generics
from rest_framework.exceptions import ValidationError


class StolenBikes(generics.ListAPIView):
    """
    Expect coordinates lon and lat in query params
    """
    serializer_class = BikePublicSerializer

    def get_queryset(self):
        queryset = []
        search_type = self.request.query_params.get('type', default="all")

        if search_type == 'all':
            queryset = Bike.objects.filter(robbed=True)

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
                                            - 'near'""")

        return queryset

    def get_by_geolocation(self, coords):
        weighted_bikes = {}
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


class CreateFoundAlert(generics.CreateAPIView):
    queryset = FoundAlert.objects.all()
    serializer_class = FoundAlertSerializer

    def perform_create(self, serializer):
        bike = Bike.objects.get(reference=self.request.data['reference'])
        serializer.save(bike=bike)
