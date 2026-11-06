# 📚 Library Management System — OOP in Python

A clean, object-oriented library system with books, magazines, DVDs, student and teacher
members, borrowing limits, late-fine calculation and JSON persistence.
Built for the *Object-Oriented Programming* course.

## OOP concepts demonstrated
| Concept | Where |
|---------|-------|
| **Abstraction** | `Item` and `Member` are abstract base classes (`ABC`) |
| **Inheritance** | `Book`, `Magazine`, `DVD` extend `Item`; `Student`, `Teacher` extend `Member` |
| **Polymorphism** | Each item type has its own `loan_days`; each member type its own `borrow_limit` and fine rate |
| **Encapsulation** | Copies are changed only through `checkout()` / `give_back()` |
| **Composition** | `Library` has items and members; `Loan` links an item with a member |
| **Custom exceptions** | `ItemUnavailable`, `BorrowLimitReached`, ... |

## Run
```bash
python main.py                     # interactive menu
python -m unittest discover tests  # run unit tests
```

## Structure
```
library/
  models.py       # Item, Book, Magazine, DVD, Member, Student, Teacher, Loan
  system.py       # Library controller + JSON save/load
  exceptions.py
tests/test_library.py
main.py           # CLI
```

## Future work
Add a GUI (Tkinter) or a REST API (FastAPI), reservations, and an SQLite backend.
