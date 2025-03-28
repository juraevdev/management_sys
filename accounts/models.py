import random, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users/profile/images/', null=True, blank=True)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
    

    def generate_verify_code(self):
        code = ''.join(str(random.randint(0, 9) for _ in range(5)))
        UserConfirmation.objects.create(
            user = self,
            code = code,
            expires = timezone.now() + datetime.timedelta(minutes=2)
        )

        return code

    

class UserConfirmation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=5)
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        f'{self.user} - {self.code}'
