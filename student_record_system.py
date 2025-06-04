import sqlite3
from tabulate import tabulate

# Database connection
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        course TEXT
    )
''')
conn.commit()


def add_student():
    try:
        name = input("Enter name: ").strip()
        age = int(input("Enter age: "))
        course = input("Enter course: ").strip()

        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
        conn.commit()
        print("✅ Student added successfully.\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Name", "Age", "Course"], tablefmt="fancy_grid"))
    else:
        print("ℹ️  No records found.\n")


def search_student():
    keyword = input("Enter student ID or Name: ").strip()
    if keyword.isdigit():
        cursor.execute("SELECT * FROM students WHERE id = ?", (int(keyword),))
    else:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f'%{keyword}%',))

    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Name", "Age", "Course"], tablefmt="fancy_grid"))
    else:
        print("❌ No matching student found.\n")


def update_student():
    sid = input("Enter student ID to update: ").strip()
    if not sid.isdigit():
        print("❌ Invalid ID.\n")
        return

    cursor.execute("SELECT * FROM students WHERE id = ?", (int(sid),))
    if not cursor.fetchone():
        print("❌ Student not found.\n")
        return

    name = input("Enter new name: ").strip()
    age = input("Enter new age: ").strip()
    course = input("Enter new course: ").strip()

    if not age.isdigit():
        print("❌ Age must be a number.\n")
        return

    confirm = input("Confirm update? (y/n): ").strip().lower()
    if confirm == 'y':
        cursor.execute("UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
                       (name, int(age), course, int(sid)))
        conn.commit()
        print("✅ Student updated.\n")
    else:
        print("❌ Update cancelled.\n")


def delete_student():
    sid = input("Enter student ID to delete: ").strip()
    if not sid.isdigit():
        print("❌ Invalid ID.\n")
        return

    cursor.execute("SELECT * FROM students WHERE id = ?", (int(sid),))
    if not cursor.fetchone():
        print("❌ Student not found.\n")
        return

    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM students WHERE id = ?", (int(sid),))
        conn.commit()
        print("✅ Student deleted.\n")
    else:
        print("❌ Deletion cancelled.\n")


def main():
    while True:
        print("\n====== Student Record Management System ======")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student (by ID or Name)")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")

    conn.close()


if __name__ == "__main__":
    main()
