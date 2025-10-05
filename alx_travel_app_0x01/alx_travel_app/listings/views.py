from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
	"""Simple CRUD for Listing.

	Anyone can list and retrieve. Auth required to create/update/delete.
	Host is set automatically from the logged in user on create.
	"""

	queryset = Listing.objects.all()
	serializer_class = ListingSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):  # set host automatically
		serializer.save(host=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
	"""Simple CRUD for Booking.

	Basic permissions: read for everyone, write requires auth.
	In a real app we'd restrict updates/cancels to owner or host.
	"""

	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):  # set user automatically if not provided
		# If client doesn't send user, fall back to request.user
		user = serializer.validated_data.get("user") or self.request.user
		serializer.save(user=user)

