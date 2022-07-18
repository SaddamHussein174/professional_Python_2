from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

rebuilt_contacts_list = []
for row in contacts_list:
    for column in range(2):
        pattern = r"\w+"
        name_list = re.findall(pattern, row[column])
        row[column] = name_list.pop(0)
        if name_list:
            row[column + 1] = ' '.join(name_list)
    pattern = r"(\+7|8)?\s*\(?(495)\)*\s*-*(\d{3})-*(\d{2})-*(\d{2})\W*(доб\. \d*)?\)?"
    if row[5] != "phone":
        result = re.sub(pattern, r"+7 (\2) \3-\4-\5 \6", row[5])
        row[5] = result
    rebuilt_contacts_list.append(row[0:7])

final_contacts_list = []
while rebuilt_contacts_list:
    base_row = rebuilt_contacts_list.pop(0)
    for row in reversed(rebuilt_contacts_list):
        if row[0:1] == base_row[0:1]:
            for cell in range(len(row)):
                if row[cell] != base_row[cell]:
                    base_row[cell] = base_row[cell] + row[cell]
            rebuilt_contacts_list.remove(row)
    final_contacts_list.append(base_row)

pprint(final_contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл

with open("phonebook.csv", "w", encoding='UTF-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)
