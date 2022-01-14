from django.db import models
from account.models import User

# Create your models here.
class Faq(models.Model):
    question = models.TextField()
    # answer = RichTextField()
    created_user = models.Foreignkey(User, on_delete=models.CASCADE, db_name="created_user")
    created_time = models.DateTimeField()
    last_modified = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "faq"