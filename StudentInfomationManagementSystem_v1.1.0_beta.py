# -- coding: utf-8 --

'''
@StudentManagementSystem
@AlanZhou
@Version 1.1.0_beta
@05/18/2024
'''

import csv
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

class Student:
    def __init__(self, student_id, name, gender, chinese_score, math_score, english_score):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.chinese_score = chinese_score
        self.math_score = math_score
        self.english_score = english_score

    def __str__(self):
        return f"学号: {self.student_id}, 姓名: {self.name}, 性别: {self.gender}, 语文成绩: {self.chinese_score}, 数学成绩: {self.math_score}, 英语成绩: {self.english_score}"

class StudentManagementSystemGUI:
    def __init__(self, master):
        self.master = master
        self.students = []
        master.title("学生信息管理系统")

        # Menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存到CSV", command=self.save_to_csv)
        file_menu.add_command(label="从CSV导入", command=self.add_students_from_csv)
        file_menu.add_command(label="退出", command=self.master.quit)

        manage_menu = tk.Menu(menu)
        menu.add_cascade(label="管理", menu=manage_menu)
        manage_menu.add_command(label="添加学生", command=self.add_student)
        manage_menu.add_command(label="删除学生", command=self.delete_student)
        manage_menu.add_command(label="显示所有学生", command=self.display_all_students)
        manage_menu.add_command(label="清空学生信息", command=self.clear_all_students)

        search_menu = tk.Menu(menu)
        menu.add_cascade(label="搜索", menu=search_menu)
        search_menu.add_command(label="查找学生", command=self.search_student)

        # Status bar
        self.status = tk.Label(master, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def add_student(self):
        def validate_and_add():
            try:
                student_id = int(entry_student_id.get())
                name = entry_name.get().strip()
                gender = gender_var.get()
                chinese_score = int(entry_chinese_score.get())
                math_score = int(entry_math_score.get())
                english_score = int(entry_english_score.get())
                if len(str(student_id)) != 5 or str(student_id)[0] == '0':
                    raise ValueError("学号格式错误，必须为五位数，且首位不能为0。")
                if any(student.student_id == student_id for student in self.students):
                    raise ValueError("该学号已存在，请使用不同的学号。")
                new_student = Student(student_id, name, gender, chinese_score, math_score, english_score)
                self.students.append(new_student)
                messagebox.showinfo("成功", "学生信息录入成功！")
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("错误", str(e))
        
        add_window = tk.Toplevel(self.master)
        add_window.title("添加学生")

        tk.Label(add_window, text="学号").grid(row=0)
        tk.Label(add_window, text="姓名").grid(row=1)
        tk.Label(add_window, text="性别").grid(row=2)
        tk.Label(add_window, text="语文成绩").grid(row=3)
        tk.Label(add_window, text="数学成绩").grid(row=4)
        tk.Label(add_window, text="英语成绩").grid(row=5)

        entry_student_id = tk.Entry(add_window)
        entry_name = tk.Entry(add_window)
        gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(add_window, textvariable=gender_var, values=["男", "女"])
        entry_chinese_score = tk.Entry(add_window)
        entry_math_score = tk.Entry(add_window)
        entry_english_score = tk.Entry(add_window)

        entry_student_id.grid(row=0, column=1)
        entry_name.grid(row=1, column=1)
        gender_combo.grid(row=2, column=1)
        entry_chinese_score.grid(row=3, column=1)
        entry_math_score.grid(row=4, column=1)
        entry_english_score.grid(row=5, column=1)

        gender_combo.current(0)  # Sets default to first item

        tk.Button(add_window, text="提交", command=validate_and_add).grid(row=6, column=0, columnspan=2)

    def display_all_students(self):
        display_window = tk.Toplevel(self.master)
        display_window.title("所有学生信息")
        text = tk.Text(display_window)
        text.pack()
        for student in self.students:
            text.insert(tk.END, str(student) + '\n')

    def clear_all_students(self):
        if messagebox.askyesno("确认", "确定清空所有学生信息？"):
            self.students = []
            messagebox.showinfo("已清空", "所有学生信息已清空！")

    def save_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV 文件", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for student in self.students:
                    writer.writerow([student.student_id, student.name, student.gender, student.chinese_score, student.math_score, student.english_score])
            messagebox.showinfo("保存成功", "学生信息已保存到CSV文件。")

    def add_students_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV 文件", "*.csv")])
        if filename:
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
                            existing_student = next((s for s in self.students if s.student_id == student_id), None)
                            if existing_student:
                                existing_student.name = name
                                existing_student.gender = gender
                                existing_student.chinese_score = chinese_score
                                existing_student.math_score = math_score
                                existing_student.english_score = english_score
                            else:
                                new_student = Student(student_id, name, gender, chinese_score, math_score, english_score)
                                self.students.append(new_student)
                        except (ValueError, IndexError):
                            messagebox.showerror("错误", "CSV文件中的数据格式错误或不完整。")
                            return
                messagebox.showinfo("成功", "学生信息从CSV文件导入成功！")
            except FileNotFoundError:
                messagebox.showerror("错误", "文件不存在！")

    def search_student(self):
        criteria = simpledialog.askstring("搜索", "请输入查询条件(例如: 学号 > 10000; 支持的运算符包括：==, >, <, >=, <=, !=, in, not in): ")
        try:
            parts = criteria.split()
            operator = parts[1] if len(parts) == 3 else parts[1] + ' ' + parts[2]
            field = parts[0]
            value = parts[2] if operator != 'not in' else parts[3]
            if operator != 'in' and operator != 'not in':
                value = int(value)
            field_map = {"学号": "student_id", "姓名": "name", "语文成绩": "chinese_score", "数学成绩": "math_score", "英语成绩": "english_score"}

            results = []
            for student in self.students:
                student_value = getattr(student, field_map.get(field, field))
                if operator == '==' and student_value == value:
                    results.append(student)
                elif operator == '!=' and student_value != value:
                    results.append(student)
                elif operator == '>' and student_value > value:
                    results.append(student)
                elif operator == '>=' and student_value >= value:
                    results.append(student)
                elif operator == '<' and student_value < value:
                    results.append(student)
                elif operator == '<=' and student_value <= value:
                    results.append(student)
                elif operator == 'in' and value in student_value:
                    results.append(student)
                elif operator == 'not in' and value not in student_value:
                    results.append(student)

            if results:
                search_window = tk.Toplevel(self.master)
                search_window.title("搜索结果")
                text = tk.Text(search_window)
                text.pack()
                for student in results:
                    text.insert(tk.END, str(student) + '\n')
            else:
                messagebox.showinfo("搜索结果", "未找到符合条件的学生！")

            if messagebox.askyesno("搜索", "是否继续查询？"):
                self.search_student()
        except ValueError:
            messagebox.showerror("错误", "查询条件格式错误！")

    def delete_student(self):
        student_id = simpledialog.askinteger("删除学生", "请输入要删除的学生学号：")
        student_to_delete = next((student for student in self.students if student.student_id == student_id), None)
        if student_to_delete:
            if messagebox.askyesno("确认删除", "确定删除以下学生信息？\n" + str(student_to_delete)):
                self.students.remove(student_to_delete)
                messagebox.showinfo("已删除", "学生信息已删除！")
        else:
            messagebox.showerror("错误", "未找到对应学号的学生信息！")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystemGUI(root)
    root.mainloop()
