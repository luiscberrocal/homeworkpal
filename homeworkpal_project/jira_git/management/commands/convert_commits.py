from django.core.management import BaseCommand

__author__ = 'lberrocal'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('folder')

    def handle(self, *args, **options):
        self.stdout.write('filename: %s' % options['filename'])