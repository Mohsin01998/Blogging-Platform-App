
from django.contrib.auth.models import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Comment(models.Model):
    body=models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,default=0)

class Profile(models.Model):
    # fields for user model
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email_token=models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

