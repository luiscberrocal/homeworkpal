from openpyxl import Workbook

from jira_git.csv import GitExportParser


class ExcelCommitImporter(object):
    '''
    Class to import list created with GitExportParser
    '''
    def __init__(self):
        self.pike_parser = GitExportParser()

    def parse_multiple_files(self, filenames, output_filename, **kwargs):
        wb = Workbook()
        sheet = wb.create_sheet(title='Supports')
        row = 1
        headers = ['Commit Hash', 'Username', 'Date', 'Description', 'Project', 'commit_type', 'issue_number']
        column = 1
        for header in headers:
            sheet.cell(column=column, row=row, value=header)
            column += 1
        for filename in filenames:
            commits = self.pike_parser.parse(filename, **kwargs)
            for commit in commits:
                row += 1
                column = 1
                sheet.cell(column=column, row=row, value=commit[0])
                column += 1
                sheet.cell(column=column, row=row, value=commit[1])
                column += 1
                sheet.cell(column=column, row=row, value=commit[2])
                column += 1
                sheet.cell(column=column, row=row, value=commit[3])
                column += 1
                sheet.cell(column=column, row=row, value=commit[4])
                column += 1
                sheet.cell(column=column, row=row, value=commit[5])
                column += 1
                sheet.cell(column=column, row=row, value=commit[6])
        wb.save(output_filename)
        return row - 1
