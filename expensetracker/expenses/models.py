from django.db import models
from django .contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"