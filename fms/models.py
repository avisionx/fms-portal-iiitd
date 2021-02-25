from django.db import models
from django.urls import reverse
from users_auth.models import CustomUser



class Complain(models.Model):

	user_name = models.CharField(max_length=100)
	user_id = models.CharField(max_length=100)

	COMPLAINT_CHOICES = (
		(1, 'House Keeping'),
		(2, 'Electricity'),
		(3, 'Others'),
	)

	complaint = models.IntegerField(
		choices=COMPLAINT_CHOICES,
		default=1
		 )

	complaint_Details = models.CharField(blank=True)
	mobile_number = models.IntegerField(max_length = 10)


	LOCATION_CHOICES = (
		(1,'Hostel'),
		(2,'Acad'),
		(3,'Library'),
		(4,'Others'),
	)

	location = models.IntegerField(
		choices=LOCATION_CHOICES,
		default=1
		 )
	sub_location = models.CharField(max_length = 100)

	PRIORITY_CHOICES = (
		(1,'HIGH'),
		(2,'LOW'),
	)
	priority = models.IntegerField(
		choices = PRIORITY_CHOICES,
		default = 2
		)
	add_info = models.CharField(blank=True)
	dt_time = models.DateTimeField(auto_now=True)
	status = models.IntegerField(default=0)



