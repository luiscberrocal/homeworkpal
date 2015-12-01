from django.core.management import BaseCommand
from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from interviews.excel import ExcelCertificateResults
from interviews.models import ElegibilityCertificate

__author__ = 'lberrocal'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='?')
        parser.add_argument('--certificate-number',
                            action='store',
                            dest='number',
                            default=None,
                            help='Certificate Number')

    def handle(self, *args, **options):
        self.stdout.write('filename: %s' % options['filename'])
        if options['filename']:
            filename = options['filename']
        else:
            name = options['number'].replace('.', '-')
            filename = filename_with_datetime(TEST_OUTPUT_PATH, 'Certificate_Results_%s.xlsx' % (name))

        excel = ExcelCertificateResults()
        certificate = ElegibilityCertificate.objects.get(number=options['number'])
        excel.export(filename, certificate)
        self.stdout.write('Wrote %s' % filename)