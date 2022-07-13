from dataclasses import field
from email.policy import default
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
REVIEWS = (
    ('N', 'Never again'),
    ('W', 'Would go back'),
)

class Blog(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'blog_id': self.id})
    



class Food(models.Model):
    date = models.DateField('Date')
    review = models.CharField(
        max_length=1,
        # add the 'choices' field option
        choices=REVIEWS,
        # set the default value for review to be 'N'
        default=REVIEWS[0][0]
    )

    # Create a blog_id FK
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_review_display()} on {self.date}"

    

class Photo(models.Model):
    url = models.CharField(max_length=200)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for blog_id: {self.blog_id} @{self.url}"