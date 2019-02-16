from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        User.objects.create_superuser(username, email, password)
        print("Created admin user '{}' ({})".format(username, email))
