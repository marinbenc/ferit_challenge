from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='solutions/')
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"

class LandingPage(models.Model):
    content = MarkdownxField()

    def __str__(self):
        return "Landing Page Content"
