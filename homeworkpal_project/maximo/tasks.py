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
        document.save()
        try:
            results = data_loader.load(document.docfile.file)
        except Exception as e:
            msg = 'Error loading file %s. %s: %s' % (document.docfile.name, type(e).__name__,  e)
            logger.error(msg)
            results = {'fatal_error': msg }
            document.status = DataDocument.FAILED
        document.results = results
        document.date_end_processing = timezone.now()
        if document.status == DataDocument.PENDING:
            document.status = DataDocument.PROCESSED
        document.save()
        logger.debug('File %s updated to status %s' % (document.docfile.name, document.status))
        return results

