from openpyxl import load_workbook
from .models import MaximoTicket

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




class MaximoDataLoader(object):
    LOAD_TICKETS = 'LOAD_TICKETS'
    LOAD_TIME = 'LOAD_TIME'

    def __init__(self, stdout=None):
        self.stdout = stdout

    def write(self, msg):
        if self.stdout:
            self.stdout.write(msg)

    def load(self, filename, action, allow_update=False,**kwargs):
        wb = load_workbook(filename=filename, data_only=True)
        if action == self.LOAD_TICKETS:
            self.load_tickets(wb,allow_update=allow_update, **kwargs)

    def load_tickets(self, wb, allow_update=False, **kwargs):
        ticket_mappings ={0: 'ticket_type',
                          1: 'number',
                          2: 'name'}
        sheet_name = kwargs.get('ticket_sheet', 'Maximo Tickets')
        ticket_sheet = wb[sheet_name]
        row_num = 1
        created = 0
        updated = 0
        for row in ticket_sheet.rows:
            if row_num > 1:
                data_dictionary = row_to_dictionary(row, ticket_mappings)
                obj, created = MaximoTicket.objects.get_or_create(ticket_type=data_dictionary['ticket_type'],
                                                                  number=data_dictionary['number'],
                                                                  defaults=data_dictionary)
                if created:
                    self.write('%d Created Maximo ticket %s' % (row_num-1, obj))
                    created += 1
                elif allow_update:
                    self.write('%d Update Maximo ticket %s' % (row_num-1, obj))
                    updated += 1
            row_num += 1
        results = {'rows_parsed': row_num-1,
                   'created': created,
                   'updated': updated,
                   'sheet': sheet_name}
        return results
