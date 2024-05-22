import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_to_db():
    db = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="student_org_app"
    )
    return db

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Organization App")
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Student Organization App")
        self.label.pack(pady=10)

        self.add_student_btn = ttk.Button(self.root, text="Add Student", command=self.add_student)
        self.add_student_btn.pack(pady=5)

        self.view_students_btn = ttk.Button(self.root, text="View Students", command=self.display_students)
        self.view_students_btn.pack(pady=5)

    def add_student(self):
        add_student_window = tk.Toplevel(self.root)
        add_student_window.title("Add Student")

        ttk.Label(add_student_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(add_student_window)
        name_entry.pack(pady=5)

        ttk.Label(add_student_window, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(add_student_window)
        email_entry.pack(pady=5)

        ttk.Label(add_student_window, text="Major:").pack(pady=5)
        major_entry = ttk.Entry(add_student_window)
        major_entry.pack(pady=5)

        ttk.Button(add_student_window, text="Save", command=lambda: self.save_student(name_entry.get(), email_entry.get(), major_entry.get())).pack(pady=10)

    def save_student(self, name, email, major):
        db = connect_to_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO students (name, email, major) VALUES (%s, %s, %s)", (name, email, major))
            db.commit()
            print("Student added successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    def view_students(self):
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()
        db.close()
        return students

    def display_students(self):
        students = self.view_students()
        view_window = tk.Toplevel(self.root)
        view_window.title("View Students")
        for student in students:
            ttk.Label(view_window, text=str(student)).pack(pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
