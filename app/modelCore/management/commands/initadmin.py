from django.conf import settings
from django.core.management.base import BaseCommand
from modelCore.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(phone="0000000000").count() == 0:
            for user in settings.ADMINS:
                name = user[0].replace(' ', '')
                phone = user[1]
                password = 'admin'
                print('Creating account for %s (%s)' % (name, phone))
                admin = User.objects.create_superuser(phone=phone, name=name, password=password)
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')