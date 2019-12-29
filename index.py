import requests,pymysql
from bs4 import BeautifulSoup

rezult = requests.get('http://edu.khsu.ru/Rating/AbitList?cg=191101&finSource=1')

parsed_html = BeautifulSoup(rezult.text,"html.parser")
students = []
types = []
dates = []
rows = 0
new_update = 0
for link in parsed_html.select("td:nth-of-type(2)"):
    student = link.get_text
    students.append(str(student))
for link in parsed_html.select("td:nth-of-type(3)"):
    date = link.get_text
    dates.append(str(date))
for link in parsed_html.select("td:nth-of-type(4)"):
    type = link.get_text
    types.append(str(type))
#-------------------- БД  ------------------
def rezult_sql(sql_zapros):
    db = pymysql.connect("localhost", "root", "", "PythonParser")
    cursor = db.cursor()

    cursor.execute(sql_zapros)
    db.commit()
    return cursor.fetchall()

sql = "SELECT COUNT(1) FROM students"
res = rezult_sql(sql)
for row in res:
    rows = row[0]


for key in range(len(students)):
    if key > rows:
        sql = "INSERT INTO students(student,date_p_d,vstupidtelnue_ekz) \
           VALUES ('%s','%s','%s')" % \
           (students[key][34:][0:-6],str(dates[key][34:][0:-6]),str(types[key][34:][0:-6]))
        rezult_sql(sql)
        new_update = key - rows
    else:
        continue
print("Добавлена " + str(new_update) + " строка!")

