# import viewsets
from rest_framework import viewsets

# import local data
from .serializers import BonafideManagementSerializer
from .models import BonafideManagement


# create a viewset
class BonafideManagementViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = BonafideManagement.objects.all()

    # specify serializer to be used
    serializer_class = BonafideManagementSerializer
