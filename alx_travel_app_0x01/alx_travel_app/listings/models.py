from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Listing(TimeStampedModel):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	location = models.CharField(max_length=255)
	price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
	max_guests = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	is_available = models.BooleanField(default=True)
	image_url = models.URLField(blank=True)
	host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:  # pragma: no cover - human readable
		return f"{self.title} - {self.location}"


class Booking(TimeStampedModel):
	STATUS_PENDING = "PENDING"
	STATUS_CONFIRMED = "CONFIRMED"
	STATUS_CANCELLED = "CANCELLED"
	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_CONFIRMED, "Confirmed"),
		(STATUS_CANCELLED, "Cancelled"),
	]

	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
	check_in = models.DateField()
	check_out = models.DateField()
	guests = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	total_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)

	class Meta:
		ordering = ["-created_at"]
		constraints = [
			models.CheckConstraint(check=models.Q(check_in__lt=models.F("check_out")), name="check_in_before_check_out"),
		]

	def __str__(self) -> str:  # pragma: no cover - human readable
		return f"Booking #{self.pk} - {self.listing.title} ({self.check_in} -> {self.check_out})"


class Review(TimeStampedModel):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	comment = models.TextField(blank=True)

	class Meta:
		ordering = ["-created_at"]
		unique_together = ("listing", "user")

	def __str__(self) -> str:  # pragma: no cover - human readable
		return f"Review {self.rating}/5 for {self.listing.title} by {self.user}"
