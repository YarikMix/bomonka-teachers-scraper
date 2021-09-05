import json

import openpyxl


def write_json(data, file_name="data"):
    with open(f"{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def write_excel(data, file_name="data"):
    book = openpyxl.Workbook()
    sheet = book.active

    sheet["A1"] = "Преподователи"
    sheet["B1"] = "Кафедра"
    sheet["C1"] = "Должность"
    for row, teacher in enumerate(data, start=2):
        sheet[row][0].value = teacher["Ф.И.О"]
        sheet[row][1].value = teacher["Кафедра"]
        sheet[row][2].value = teacher["Должность"]

    book.save(f"{file_name}.xlsx")
    book.close()