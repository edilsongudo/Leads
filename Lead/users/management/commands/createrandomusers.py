from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random


class Command(BaseCommand):
    help = '''
    This command creates random users and saves them in a file
    Args: <amount>
    '''

    def add_arguments(self, parser):
        parser.add_argument('amount')

    def generate_user(self):
        with open('first-names.txt', 'r') as f:
            names = f.readlines()

        username = random.choice(names).lower().strip()
        email = f'{username}@gmail.com'
        password = 'randompassword'

        User = get_user_model()
        User.objects.create_user(
            username=username, email=email, password=password)

        with open('generatedusers.txt', 'a') as f:
            f.write(f'{username},{email},{password}')

    def handle(self, *args, **options):
        for i in range(int(options['amount'])):
            self.generate_user()
        self.stdout.write('Users created')
