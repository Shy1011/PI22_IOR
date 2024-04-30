import xlwings as xw

def initialize_excel(filepath):
    app = xw.App(visible=False)
    wb = app.books.add()
    return app, wb

def finalize_excel(app, wb, filepath):
    wb.save(filepath)
    wb.close()
    app.quit()

def write(sheet, name1, name2, name3):
    # 找到第一个空白行
    row = 1
    while sheet.range(f'A{row}').value is not None:
        row += 1
    # 在找到的空白行填充数据
    sheet.range(f'A{row}').value = name1
    sheet.range(f'A{row + 1}').value = name2
    sheet.range(f'A{row + 2}').value = name3

def data_insert(sheet, data, row):
    col = 1
    while sheet.range(row, col).value is not None:
        col += 1
    sheet.range(row, col).value = data

if __name__ == "__main__":
    # 使用示例
    app, wb = initialize_excel('../results/example.xlsx')
    sheet = wb.sheets[0]

    write(sheet, '张三', '李四', '王五')
    data_insert(sheet, 'data1', 1)
    data_insert(sheet, 'data2', 1)
    data_insert(sheet, 'data3', 1)
    data_insert(sheet, 'data1', 2)
    data_insert(sheet, 'data2', 2)
    data_insert(sheet, 'data3', 2)

    finalize_excel(app, wb, '../results/example.xlsx')