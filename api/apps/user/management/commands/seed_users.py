from django.core.management.base import BaseCommand

from apps.user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create_user(username="admin", email="admin@admin.com", is_superuser=True, is_staff=True)
        user.set_password("123456@aA")
        user.save()
