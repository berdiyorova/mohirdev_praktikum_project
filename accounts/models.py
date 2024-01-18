from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
# Modelga field qo'shish

# 1-usul  AbstractUserdan meros olish (inherit qilish)

# Bu usuldan boshida, model yaratilayotgan paytda foydalangan ma'qul. Sababi uni yangitdan migrate qilish kk va bunda
# bazadagi mavjud ma'lumotlar o'chib ketadi
# class User(AbstractUser):
#     photo = models.ImageField()
#     date_of_birth = models.DateField()
#     address = models.TextField()


# 2-usul  yangi model yaratib avvalgisiga ulab qo'yiladi:

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profili"
