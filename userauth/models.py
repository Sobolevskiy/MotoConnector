import secrets
from datetime import datetime, timezone

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class PendingUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')
    verification_code = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.verification_code = secrets.token_hex(8)

    def is_valid(self, code) -> bool:
        """10 mins OTP validation"""
        lifespan_in_seconds = float(10 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds or self.verification_code != code:
            return False

        return True


@receiver(pre_save, sender=PendingUser)
def generate_verification_code(sender, instance, **kwargs):
    instance.generate_code()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone = PhoneNumberField(region="RU")
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    verified = models.BooleanField(default=False)

    def generate_verification(self):
        return PendingUser.objects.create(user=self.user)


@receiver(post_save, sender=User)
def create_user_profile_and_token(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
