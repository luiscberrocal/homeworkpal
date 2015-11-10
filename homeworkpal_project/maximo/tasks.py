from celery.task import Task
from django.utils import timezone
from maximo.excel import MaximoExcelData
from maximo.models import DataDocument
import  logging
__author__ = 'lberrocal'
logger = logging.getLogger(__name__)

class ProcessExcelTask(Task):

    def run(self, document_id, **kwargs):
        try:
            document = DataDocument.objects.get(pk=document_id)
        except:
            logger.warn('Could not find document with id %d' % document_id)
            return None
        data_loader = MaximoExcelData()
        document.date_start_processing = timezone.now()
        results = data_loader.load(document.docfile.file)
        document.results = results
        document.save()
        logger.debug('File %s updated' % (document.docfile.name))
        return results

