"""Command-line interface for the Library Management System."""
import os

from library import Book, DVD, Library, LibraryError, Magazine, Student, Teacher

DATA_FILE = "library_data.json"


def seed(lib):
    lib.add_item(Book("B1", "Python Crash Course", "Eric Matthes", 2))
    lib.add_item(Book("B2", "Artificial Intelligence: A Modern Approach", "Russell & Norvig", 1))
    lib.add_item(Magazine("M1", "AI Weekly", "Issue 42"))
    lib.add_item(DVD("D1", "The Social Dilemma", 94))
    lib.add_member(Student("S1", "Anaya"))
    lib.add_member(Teacher("T1", "Dr. Khan"))


MENU = """
1. List items      2. Search        3. Borrow
4. Return         5. Members       6. Overdue
7. Save & quit
"""


def main():
    lib = Library.load(DATA_FILE) if os.path.exists(DATA_FILE) else Library()
    if not lib.items:
        seed(lib)
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                for item in lib.items.values():
                    print(item)
            elif choice == "2":
                for item in lib.search(input("Search: ")):
                    print(item)
            elif choice == "3":
                loan = lib.borrow(input("Member id: "), input("Item id: "))
                print(f"Borrowed! Due on {loan.due_date}")
            elif choice == "4":
                fine = lib.give_back(input("Member id: "), input("Item id: "))
                print(f"Returned. Fine: Rs {fine}")
            elif choice == "5":
                for member in lib.members.values():
                    print(member)
            elif choice == "6":
                late = lib.overdue()
                print("\n".join(f"{l.member.name}: {l.item.title} (due {l.due_date})" for l in late) or "Nothing overdue")
            elif choice == "7":
                lib.save(DATA_FILE)
                print("Saved. Bye!")
                break
        except LibraryError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
