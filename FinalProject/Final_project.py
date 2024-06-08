import csv
import os
import re

class Student:
    def __init__(self, id, name, gender, chinese, math, english):
        self.id = id
        self.name = name
        self.gender = gender
        self.chinese = chinese
        self.math = math
        self.english = english

    def __str__(self):
        return f'{self.id},{self.name},{self.gender},{self.chinese},{self.math},{self.english}'

class StudentManagementSystem:
    def __init__(self, filename='students.csv'):
        self.filename = filename
        self.students = {}
        self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 6:
                        student = Student(*row)
                        self.students[student.id] = student

    def save_students(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            for student in self.students.values():
                writer.writerow([student.id, student.name, student.gender, student.chinese, student.math, student.english])

    def add_student(self, id, name, gender, chinese, math, english):
        if id.isdigit() and len(id) == 5 and id[0] != '0':
            if 0 <= int(chinese) <= 100 and 0 <= int(math) <= 100 and 0 <= int(english) <= 100:
                self.students[id] = Student(id, name, gender, chinese, math, english)
                print("学生信息录入成功")
            else:
                print("成绩必须在0到100之间")
        else:
            print("学号必须是5位且第一位不能为0")

    def input_student(self):
        while True:
            data = input("请输入学生信息（格式：学号,姓名,性别,语文成绩,数学成绩,英语成绩）：")
            parts = data.split(',')
            if len(parts) == 6:
                self.add_student(*parts)
            else:
                print("输入格式不正确")
            cont = input("是否继续输入？(y/n)：")
            if cont.lower() != 'y':
                break

    def import_from_csv(self):
        filename = input("请输入CSV文件名：")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 6:
                        student_id = row[0]
                        existing_student = self.find_student_by_id(student_id)
                        if existing_student is not None:
                            # 更新已有学生的信息
                            existing_student.name = row[1]
                            existing_student.chinese_score = row[2]
                            existing_student.math_score = row[3]
                            existing_student.english_score = row[4]
                            existing_student.total_score = row[5]
                        else:
                            # 添加新的学生
                            self.add_student(*row)
            print("文件导入成功")
        else:
            print("文件不存在")

    def find_student_by_id(self, student_id):
        for student in self.students.values():
            if student.id == student_id:
                return student
        return None

    def find_students(self):
        field_map = {"学号": "id", "姓名": "name", "性别": "gender", "语文成绩": "chinese", "数学成绩": "math", "英语成绩": "english"}
        while True:
            query = input("请输入查询条件（例如：学号 > 12345，支持比较运算法（ >, >=, ==, !=, <, <=）和成员运算法（ in, not in））：")
            match = re.match(r'(\w+)\s*(==|!=|>|>=|<|<=|in|not in)\s*(.+)', query)
            if match:
                key, op, value = match.groups()
                if op in ['in', 'not in']:
                    key, value = value, key
                key = field_map.get(key, key)  # 将中文字段映射到英文属性名
                if key not in ['id', 'name', 'gender', 'chinese', 'math', 'english']:
                    print("无效的查询字段")
                    continue
                results = []
                for student in self.students.values():
                    if self.compare(getattr(student, key), op, value):
                        results.append(student)
                if results:
                    for result in results:
                        print(result)
                else:
                    print("没有符合条件的学生信息")
            else:
                print("查询条件格式不正确")

            cont = input("是否继续查询？(y/n)：")
            if cont.lower() != 'y':
                break

    def compare(self, a, op, b):
        if op in ['in', 'not in']:
            if op == 'in':
                return b in a
            else:
                return b not in a

        # 尝试将字符串转为数值比较
        try:
            a = float(a)
            b = float(b)
        except ValueError:
            pass

        if op == '>':
            return a > b
        elif op == '>=':
            return a >= b
        elif op == '==':
            return a == b
        elif op == '!=':
            return a != b
        elif op == '<':
            return a < b
        elif op == '<=':
            return a <= b
        return False

    def delete_student(self):
        self.find_students()
        id = input("请输入要删除的学生的学号：")
        if id in self.students:
            del self.students[id]
            print("学生信息删除成功")
        else:
            print("未找到该学号的学生信息")

    def display_all_students(self):
        if self.students:
            for student in self.students.values():
                print(student)
        else:
            print("没有学生信息")

    def clear_students(self):
        confirm = input("确认清空所有学生信息？(y/n)：")
        if confirm.lower() == 'y':
            self.students.clear()
            print("所有学生信息已清空")

    def run(self):
        while True:
            print("1. 录入学生信息")
            print("2. 从CSV文件导入学生信息")
            print("3. 查找学生信息")
            print("4. 删除学生信息")
            print("5. 显示所有学生信息")
            print("6. 清空所有学生信息")
            print("7. 退出系统")
            choice = input("请选择功能：")
            if choice == '1':
                self.input_student()
            elif choice == '2':
                self.import_from_csv()
            elif choice == '3':
                self.find_students()
            elif choice == '4':
                self.delete_student()
            elif choice == '5':
                self.display_all_students()
            elif choice == '6':
                self.clear_students()
            elif choice == '7':
                self.save_students()
                print("系统已退出")
                break
            else:
                print("无效的选择，请重新选择")

if __name__ == "__main__":
    sms = StudentManagementSystem()
    sms.run()
