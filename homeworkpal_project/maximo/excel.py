from openpyxl import load_workbook, Workbook
from .models import MaximoTicket

import logging

logger = logging.getLogger(__name__)
__author__ = 'lberrocal'

def row_to_dictionary(excel_row, mappings):
    data = dict()
    value_list = list()
    for cell in excel_row:
        if cell.value:
            value_list.append(cell.value)
        else:
            value_list.append(None)
    i = 0
    for val in value_list:
        key_name = mappings[i]
        data[key_name] = val
        i += 1

    return data


class MaximoExcelData(object):
    LOAD_TICKETS = 'LOAD_TICKETS'
    LOAD_TIME = 'LOAD_TIME'

    def __init__(self, stdout=None):
        self.ticket_mappings = {0: 'ticket_type', 1: 'number', 2: 'name'}
        self.ticket_sheet = 'Maximo Tickets'
        self.stdout = stdout

    def write(self, msg):
        if self.stdout:
            self.stdout.write(msg)

    def load(self, filename, action, allow_update=False,**kwargs):
        wb = load_workbook(filename=filename, data_only=True)
        if action == self.LOAD_TICKETS:
            ticket_results = self.load_tickets(wb,allow_update=allow_update, **kwargs)
        return {'ticket_results': ticket_results}

    def save_tickets(self, filename, tickets):
        wb = Workbook()
        sheet = wb.create_sheet(title=self.ticket_sheet)
        row = 1
        for column, v in self.ticket_mappings.items():
            sheet.cell(column=column+1, row=row, value=v.upper())
        row += 1
        for ticket in tickets:
            for column, v in self.ticket_mappings.items():
                sheet.cell(column=column+1, row=row, value=getattr(ticket, v))
            row += 1

        wb.save(filename)

    def load_tickets(self, wb, allow_update=False, **kwargs):
        sheet_name = kwargs.get('ticket_sheet', self.ticket_sheet)
        ticket_sheet = wb[sheet_name]
        row_num = 1
        created_count = 0
        updated = 0
        for row in ticket_sheet.rows:
            if row_num > 1:
                data_dictionary = row_to_dictionary(row, self.ticket_mappings)
                obj, created = MaximoTicket.objects.get_or_create(ticket_type=data_dictionary['ticket_type'],
                                                                  number=data_dictionary['number'],
                                                                  defaults=data_dictionary)
                if created:
                    self.write('%d Created Maximo ticket %s' % (row_num-1, obj))
                    logger.debug('%d Created Maximo ticket %s' % (row_num-1, obj))
                    created_count += 1
                    #logger.debug('--- %d tickets created' % created)
                elif allow_update:
                    self.write('%d Update Maximo ticket %s' % (row_num-1, obj))
                    logger.debug('%d Update Maximo ticket %s' % (row_num-1, obj))
                    updated += 1
                else:
                    logger.debug('%d Existeds Maximo ticket %s' % (row_num-1, obj))
            row_num += 1
        #logger.debug('%d tickets created' % created)
        results = {'rows_parsed': row_num-2,
                   'created': created_count,
                   'updated': updated,
                   'sheet': sheet_name}
        return results
