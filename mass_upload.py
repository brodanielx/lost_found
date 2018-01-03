import os
import openpyxl
import string

workbook = openpyxl.load_workbook('mass_upload.xlsx')

sheet_names = workbook.get_sheet_names()

sheet = workbook.get_sheet_by_name(sheet_names[0])

columns = list(string.ascii_uppercase)[1:10]

print(columns)
