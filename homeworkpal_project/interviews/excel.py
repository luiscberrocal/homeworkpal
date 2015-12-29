from openpyxl import Workbook

__author__ = 'LBerrocal'

class ExcelCertificateResults(object):

    def export(self, filename, certificate):
        wb = Workbook()
        sheet = wb.create_sheet(title='Resultados')
        row = 1
        headers = ['Reultado de la Selección', 'Cédula', 'Nombre', 'Entrevistadores', 'Comentarios']
        column = 1
        for header in headers:
            sheet.cell(column=column, row=row, value=header)
            column += 1
        for candidate in certificate.candidates.all():
            row += 1
            column = 1
            sheet.cell(column=column, row=row, value=str(candidate.certificate_result))
            column += 1
            sheet.cell(column=column, row=row, value=str(candidate.candidate.national_id))
            column += 1
            sheet.cell(column=column, row=row, value=str(candidate.candidate))
            column += 1
            sheet.cell(column=column, row=row, value='Luis Berrocal')
            column += 1
            sheet.cell(column=column, row=row, value=candidate.explanation)


        wb.save(filename)

