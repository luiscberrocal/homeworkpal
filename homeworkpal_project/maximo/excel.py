from datetime import datetime
from decimal import Decimal
from openpyxl import load_workbook, Workbook
from employee.models import Employee
from .models import MaximoTicket, MaximoTimeRegister

import logging

logger = logging.getLogger(__name__)
__author__ = 'lberrocal'


def row_to_dictionary(excel_row, mappings):
    data = dict()
    for attribute, position in mappings.items():
        data[attribute] = excel_row[position].value
    return data


def parse_hours(str_hours):
    parts = str_hours.split(':')
    return Decimal(parts[0]) + Decimal(parts[1]) /60

def parse_datetime_hours(hours):
    return hours.hour + hours.minute /60

    # data = dict()
    # value_list = list()
    # for cell in excel_row:
    #     if cell.value:
    #         value_list.append(cell.value)
    #     else:
    #         value_list.append(None)
    # i = 0
    # for val in value_list:
    #     key_name = mappings[i]
    #     data[key_name] = val
    #     i += 1
    # return data

def row_to_register_dictionary(excel_row, mappings):
    pass



class MaximoExcelData(object):
    LOAD_TICKETS = 'LOAD_TICKETS'
    LOAD_TIME = 'LOAD_TIME'

    def __init__(self, stdout=None):
        self.ticket_mappings = {'ticket_type': 0 , 'number': 1, 'name': 2}
        self.time_register_mappings = {'company_id': 0,
                                       'regular_hours': 1,
                                       'date': 2,
                                       'username': 3,
                                       'pay_rate': 5,
                                       'wo_number': 6,
                                       'ticket_type': 7,
                                       'ticket_number':8}
        self.ticket_sheet = 'Maximo Tickets'
        self.time_sheet = 'Time'
        self.stdout = stdout

    def write(self, msg):
        if self.stdout:
            self.stdout.write(msg)

    def load(self, filename, action=None, allow_update=False, **kwargs):
        wb = load_workbook(filename=filename, data_only=True)
        ticket_results = dict()
        time_results = dict()
        if action == self.LOAD_TICKETS:
            ticket_results = self.load_tickets(wb, allow_update=allow_update, **kwargs)
        elif action == self.LOAD_TIME:
            time_results = self.load_time_registers(wb, allow_update=allow_update, **kwargs)
        elif action is None:
            ticket_results = self.load_tickets(wb, allow_update=allow_update, **kwargs)
            time_results = self.load_time_registers(wb, allow_update=allow_update, **kwargs)
        else:
            raise ValueError('"%s" is an invalida action for load' % action)

        return {'ticket_results': ticket_results,
                'time_results': time_results}

    def save_tickets(self, filename, tickets):
        wb = Workbook()
        sheet = wb.create_sheet(title=self.ticket_sheet)
        row = 1
        for v, column in self.ticket_mappings.items():
            sheet.cell(column=column + 1, row=row, value=v.upper())
        row += 1
        for ticket in tickets:
            for v,column, in self.ticket_mappings.items():
                sheet.cell(column=column + 1, row=row, value=getattr(ticket, v))
            row += 1

        wb.save(filename)

    def save_time_registers(self, filename, registers):
        wb = Workbook()
        sheet = wb.create_sheet(title=self.ticket_sheet)
        row = 1
        for v, column in self.time_register_mappings.items():
            sheet.cell(column=column + 1, row=row, value=v.upper())
        row += 1
        for register in registers:
            col = self.time_register_mappings['company_id'] + 1
            sheet.cell(column=col, row=row, value=register.employee.company_id)
            col = self.time_register_mappings['regular_hours'] + 1
            sheet.cell(column=col, row=row, value=register.regular_hours)
            col = self.time_register_mappings['date'] + 1
            sheet.cell(column=col, row=row, value=register.date)
            col = self.time_register_mappings['username'] + 1
            sheet.cell(column=col, row=row, value=register.employee.user.username)
            col = self.time_register_mappings['pay_rate'] + 1
            sheet.cell(column=col, row=row, value=register.pay_rate)
            if register.ticket.ticket_type == MaximoTicket.MAXIMO_WORKORDER:
                col = self.time_register_mappings['wo_number'] + 1
                sheet.cell(column=col, row=row, value=register.ticket.number)
            if register.ticket.ticket_type != MaximoTicket.MAXIMO_WORKORDER:
                col = self.time_register_mappings['ticket_type'] + 1
                sheet.cell(column=col, row=row, value=register.ticket.ticket_type)
                col = self.time_register_mappings['ticket_number'] + 1
                sheet.cell(column=col, row=row, value=register.ticket.number)
            row += 1
        wb.save(filename)

    def load_time_registers(self, wb, allow_update=False, **kwargs):
        sheet_name = kwargs.get('Time', self.time_sheet)
        time_sheet = wb[sheet_name]
        results = {'rows_parsed': 0,
                   'created': 0,
                   'sheet': sheet_name,
                   'errors': list()}
        row_num = 1
        created_count = 0
        updated = 0
        errors = list()
        for row in time_sheet.rows:
            if row_num > 1:
                attributes = dict()
                company_id = row[self.time_register_mappings['company_id']].value
                try:
                    attributes['employee'] = Employee.objects.get(company_id=company_id)
                    attributes['date'] = row[self.time_register_mappings['date']].value
                    ticket_type = row[self.time_register_mappings['ticket_type']].value
                    if ticket_type not in [MaximoTicket.MAXIMO_SR]:
                        ticket_type = MaximoTicket.MAXIMO_WORKORDER
                    #attributes['date'] = datetime.strptime(str_register_date, '%m/%d/%Y')
                    attributes['pay_rate'] = Decimal(row[self.time_register_mappings['pay_rate']].value)
                    if ticket_type == MaximoTicket.MAXIMO_WORKORDER:
                        number = row[self.time_register_mappings['wo_number']].value
                    else:
                        number = row[self.time_register_mappings['ticket_number']].value
                    attributes['ticket'] = MaximoTicket.objects.get(ticket_type=ticket_type, number=number)
                    attributes['regular_hours'] =  parse_datetime_hours(row[self.time_register_mappings['regular_hours']].value)
                    MaximoTimeRegister.objects.create(**attributes)
                    created_count += 1
                except Employee.DoesNotExist:
                    username = row[self.time_register_mappings['username']].value
                    msg = 'Employee with id %s and username %s ' \
                          'on row %d does not exist time registe was not loaded' % (company_id, username, row_num)
                    logger.warn(msg)
                    error = {'row_num': row_num,
                             'type': 'Employee does not exist',
                             'message':msg}
                    errors.append(error)
                except MaximoTicket.DoesNotExist:
                    msg = '%s with number %s on line %d does not exist' % (ticket_type, number, row_num)
                    logger.warn(msg)
                    error = {'row_num': row_num,
                             'type': 'Ticket does not exist',
                             'message':msg}
                    errors.append(error)
                except TypeError as te:
                    msg = 'Unexeptected error %s on row %d' % (te, row_num)
                    logger.error()
                    error = {'row_num': row_num,
                             'type': 'Unexeptected Type Error',
                             'message': msg}
                    errors.append(error)
            row_num +=1
        results = {'rows_parsed': row_num - 2,
                   'created': created_count,
                   'sheet': sheet_name,
                   'errors': errors}
        return results

    def load_tickets(self, wb, allow_update=False, **kwargs):
        sheet_name = kwargs.get('ticket_sheet', self.ticket_sheet)
        ticket_sheet = wb[sheet_name]
        results = {'rows_parsed': 0,
                   'created': 0,
                   'updated': 0,
                   'sheet': sheet_name}
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
                    self.write('%d Created Maximo ticket %s' % (row_num - 1, obj))
                    logger.debug('%d Created Maximo ticket %s' % (row_num - 1, obj))
                    created_count += 1
                    # logger.debug('--- %d tickets created' % created)
                elif allow_update:
                    self.write('%d Update Maximo ticket %s' % (row_num - 1, obj))
                    logger.debug('%d Update Maximo ticket %s' % (row_num - 1, obj))
                    updated += 1
                else:
                    logger.debug('%d Existed Maximo ticket %s' % (row_num - 1, obj))
            row_num += 1
        # logger.debug('%d tickets created' % created)
        results = {'rows_parsed': row_num - 2,
                   'created': created_count,
                   'updated': updated,
                   'sheet': sheet_name}
        return results
