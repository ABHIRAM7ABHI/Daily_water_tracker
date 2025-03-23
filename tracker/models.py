from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.quantity}L on {self.date}"
