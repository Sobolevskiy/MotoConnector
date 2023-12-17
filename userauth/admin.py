from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from userauth.models import PendingUser, UserProfile
from userauth.utils import send_sync_verification_email


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    actions = ['resend_email']

    def resend_email(self, request, queryset):
        for user in queryset:
            verification = user.user_profile.generate_verification()
            send_sync_verification_email(user.email, verification.verification_code)
        self.message_user(request, 'Переотправка завершена')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PendingUser)
