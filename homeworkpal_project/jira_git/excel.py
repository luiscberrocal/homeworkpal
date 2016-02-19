import os

from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment

from jira_git.csv import GitExportParser


class ExcelCommitImporter(object):
    '''
    Class to import list created with GitExportParser
    '''
    border = Border(left=Side(border_style='thin', color='FF000000'),
                    right=Side(border_style='thin', color='FF000000'),
                    top=Side(border_style='thin', color='FF000000'),
                    bottom=Side(border_style='thin', color='FF000000'),
                    diagonal=Side(border_style=None, color='FF000000'),
                    diagonal_direction=0,
                    outline=Side(border_style=None,
                                 color='FF000000'),
                    vertical=Side(border_style=None,
                                  color='FF000000'),
                    horizontal=Side(border_style=None,
                                    color='FF000000')
                    )

    alignment=Alignment(horizontal='general',
                            vertical='top',
                            text_rotation=0,
                            wrap_text=True,
                            shrink_to_fit=False,
                            indent=0)
    def __init__(self):
        self.pike_parser = GitExportParser()

    def parse_folder(self, folder, output_filename, **kwargs):
        file_list= list()
        for root, dir, files in os.walk(folder):
            for file in files:
                filename = os.path.join(root, file)
                file_list.append(filename)
        return self.parse_multiple_files(file_list, output_filename, **kwargs)

    def parse_multiple_files(self, filenames, output_filename, **kwargs):
        wb = Workbook()
        sheet = wb.create_sheet(title='Commits')
        self.setup_column_width(sheet)
        row = 1
        headers = ['Commit Hash', 'Username', 'Date', 'Description', 'Project', 'commit_type', 'issue_number', 'source_file']
        column = 1
        for header in headers:
            sheet.cell(column=column, row=row, value=header)
            column += 1
        for filename in filenames:
            commits = self.pike_parser.parse(filename, **kwargs)
            for commit in commits:
                row += 1
                column = 1
                current_cell=sheet.cell(column=column, row=row, value=commit[0])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[1])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[2])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[3])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[4])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[5])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[6])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

                column += 1
                current_cell=sheet.cell(column=column, row=row, value=commit[7])
                current_cell.alignment = self.alignment
                current_cell.border = self.border

        wb.save(output_filename)
        return row - 1

    def setup_column_width(self, sheet):
        sheet.column_dimensions['A'].width = 11
        sheet.column_dimensions['B'].width = 11
        sheet.column_dimensions['C'].width = 19
        sheet.column_dimensions['D'].width = 50
        sheet.column_dimensions['E'].width = 16
        sheet.column_dimensions['F'].width = 11
        sheet.column_dimensions['G'].width = 12
        sheet.column_dimensions['H'].width = 12