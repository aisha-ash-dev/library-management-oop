import os
import sys
import tempfile
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library import Book, DVD, Library, Student, Teacher
from library.exceptions import BorrowLimitReached, ItemUnavailable


def make_lib():
    lib = Library()
    lib.add_item(Book("B1", "Python", "Matthes", 1))
    lib.add_item(DVD("D1", "Movie", 90))
    lib.add_member(Student("S1", "Anaya"))
    lib.add_member(Teacher("T1", "Khan"))
    return lib


class TestLibrary(unittest.TestCase):
    def test_borrow_and_return(self):
        lib = make_lib()
        lib.borrow("S1", "B1")
        self.assertEqual(lib.items["B1"].available, 0)
        self.assertEqual(lib.give_back("S1", "B1"), 0)
        self.assertEqual(lib.items["B1"].available, 1)

    def test_no_copies_left(self):
        lib = make_lib()
        lib.borrow("S1", "B1")
        with self.assertRaises(ItemUnavailable):
            lib.borrow("T1", "B1")

    def test_student_limit(self):
        lib = Library()
        lib.add_member(Student("S1", "A"))
        for i in range(4):
            lib.add_item(Book(f"B{i}", "t", "a"))
        for i in range(3):
            lib.borrow("S1", f"B{i}")
        with self.assertRaises(BorrowLimitReached):
            lib.borrow("S1", "B3")

    def test_fine_polymorphism(self):
        lib = make_lib()
        old = date.today() - timedelta(days=24)            # book due after 14 days -> 10 days late
        lib.borrow("S1", "B1", old)
        self.assertEqual(lib.give_back("S1", "B1"), 100)   # student: 10 x Rs10
        lib.borrow("T1", "B1", old)
        self.assertEqual(lib.give_back("T1", "B1"), 50)    # teacher: 10 x Rs5

    def test_save_load(self):
        lib = make_lib()
        lib.borrow("S1", "D1")
        path = os.path.join(tempfile.mkdtemp(), "d.json")
        lib.save(path)
        again = Library.load(path)
        self.assertEqual(again.items["D1"].available, 0)
        self.assertEqual(len(again.members["S1"].loans), 1)


if __name__ == "__main__":
    unittest.main()
