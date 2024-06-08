# -- coding: utf-8 --

'''
@StudentManagementSystem
@AlanZhou
@Version 0.0.2
@04/15/2024
'''

import csv

class StudentManagementSystem:
    def __init__(self):
        self.students = []

    def menu(self):
        print("欢迎使用学生信息管理系统！")
        print("1. 录入学生信息")
        print("2. 从csv文件录入学生信息")
        print("3. 查找学生信息")
        print("4. 删除学生信息")
        print("5. 显示所有学生信息")
        print("6. 清空所有学生信息")
        print("7. 退出系统")

    def run(self):
        while True:
            self.menu()
            choice = input("请输入功能对应的数字：")
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.add_students_from_csv()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.delete_student()
            elif choice == '5':
                self.display_all_students()
            elif choice == '6':
                self.clear_all_students()
            elif choice == '7':
                self.save_to_csv()
                print("感谢使用！")
                break
            else:
                print("请输入正确的数字！")

    def add_student(self):
        while True:
            student_info = input("请输入学生信息(学号,姓名,性别,语文成绩,数学成绩,英语成绩)，以逗号分隔：")
            info_list = student_info.split(',')
            if len(info_list) != 6:
                print("输入格式错误，请重新输入！")
                continue
            try:
                student_id = int(info_list[0])
                name = info_list[1]
                gender = info_list[2]
                chinese_score = int(info_list[3])
                math_score = int(info_list[4])
                english_score = int(info_list[5])
            except ValueError:
                print("成绩必须为整数，请重新输入！")
                continue
            if len(str(student_id)) != 5 or str(student_id)[0] == '0':
                print("学号格式错误，请重新输入！")
                continue
            if self.check_student_id_exist(student_id):
                print("该学号已存在，请重新输入！")
                continue
            self.students.append({
                '学号': student_id,
                '姓名': name,
                '性别': gender,
                '语文成绩': chinese_score,
                '数学成绩': math_score,
                '英语成绩': english_score
            })
            print("学生信息录入成功！")
            if input("是否继续录入学生信息？(y/n)") != 'y':
                break

    def check_student_id_exist(self, student_id):
        for student in self.students:
            if student['学号'] == student_id:
                return True
        return False

    def add_students_from_csv(self):
        filename = input("请输入CSV文件名：")
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        student_id = int(row[0])
                        name = row[1]
                        gender = row[2]
                        chinese_score = int(row[3])
                        math_score = int(row[4])
                        english_score = int(row[5])
                    except (ValueError, IndexError):
                        print("文件格式错误！")
                        return
                    self.students.append({
                        '学号': student_id,
                        '姓名': name,
                        '性别': gender,
                        '语文成绩': chinese_score,
                        '数学成绩': math_score,
                        '英语成绩': english_score
                    })
            print("学生信息从CSV文件录入成功！")
        except FileNotFoundError:
            print("文件不存在！")

    def search_student(self):
        criteria = input("请输入查询条件(例如: 学号 > 10000): ")
        try:
            field, operator, value = criteria.split()
            value = int(value)
        except ValueError:
            print("查询条件格式错误！")
            return

        results = []
        for student in self.students:
            if operator == '==':
                if student[field] == value:
                    results.append(student)
            elif operator == '!=':
                if student[field] != value:
                    results.append(student)
            elif operator == '>':
                if student[field] > value:
                    results.append(student)
            elif operator == '>=':
                if student[field] >= value:
                    results.append(student)
            elif operator == '<':
                if student[field] < value:
                    results.append(student)
            elif operator == '<=':
                if student[field] <= value:
                    results.append(student)
            else:
                print("不支持的运算符！")
                return
        
        if results:
            print("查询结果：")
            for student in results:
                print(student)
        else:
            print("未找到符合条件的学生！")

    def delete_student(self):
        student_id = int(input("请输入要删除的学生学号："))
        for student in self.students:
            if student['学号'] == student_id:
                print("找到学生信息：")
                print(student)
                confirm = input("是否确认删除？(y/n)")
                if confirm == 'y':
                    self.students.remove(student)
                    print("学生信息已删除！")
                return
        print("未找到对应学号的学生信息！")

    def display_all_students(self):
        if not self.students:
            print("暂无学生信息！")
            return
        print("所有学生信息：")
        for student in self.students:
            print(student)

    def clear_all_students(self):
        if input("确定清空所有学生信息？(y/n)") == 'y':
            self.students = []
            print("所有学生信息已清空！")

    def save_to_csv(self):
        filename = input("请输入保存CSV文件名：")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for student in self.students:
                writer.writerow([
                    student['学号'],
                    student['姓名'],
                    student['性别'],
                    student['语文成绩'],
                    student['数学成绩'],
                    student['英语成绩']
                ])

if __name__ == "__main__":
    sms = StudentManagementSystem()
    sms.run()
