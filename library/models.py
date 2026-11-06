"""Domain classes. Demonstrates: abstraction, inheritance, polymorphism, encapsulation."""
from abc import ABC, abstractmethod
from datetime import date, timedelta


# ----------------------------------------------------------------- items
class Item(ABC):
    """Abstract base class for anything the library can lend."""

    def __init__(self, item_id, title, copies=1):
        self.item_id = item_id
        self.title = title
        self._available = copies   # encapsulated: change only via checkout()/give_back()
        self.total = copies

    @property
    def available(self):
        return self._available

    def checkout(self):
        if self._available <= 0:
            return False
        self._available -= 1
        return True

    def give_back(self):
        if self._available < self.total:
            self._available += 1

    @property
    @abstractmethod
    def loan_days(self):
        """Each item type has its own loan period (polymorphism)."""

    @property
    @abstractmethod
    def kind(self):
        ...

    @abstractmethod
    def details(self):
        ...

    def to_dict(self):
        return {"kind": self.kind, "id": self.item_id, "title": self.title,
                "total": self.total, "available": self._available, **self._extra()}

    def _extra(self):
        return {}

    def __str__(self):
        return f"[{self.kind}] {self.item_id}: {self.title} ({self._available}/{self.total} available)"


class Book(Item):
    kind = "Book"
    loan_days = 14

    def __init__(self, item_id, title, author, copies=1):
        super().__init__(item_id, title, copies)
        self.author = author

    def details(self):
        return f"{self.title} by {self.author}"

    def _extra(self):
        return {"author": self.author}


class Magazine(Item):
    kind = "Magazine"
    loan_days = 7

    def __init__(self, item_id, title, issue, copies=1):
        super().__init__(item_id, title, copies)
        self.issue = issue

    def details(self):
        return f"{self.title}, issue {self.issue}"

    def _extra(self):
        return {"issue": self.issue}


class DVD(Item):
    kind = "DVD"
    loan_days = 3

    def __init__(self, item_id, title, minutes, copies=1):
        super().__init__(item_id, title, copies)
        self.minutes = minutes

    def details(self):
        return f"{self.title} ({self.minutes} min)"

    def _extra(self):
        return {"minutes": self.minutes}


# --------------------------------------------------------------- members
class Member(ABC):
    FINE_PER_DAY = 10   # rupees

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.loans = []   # list of Loan objects

    @property
    @abstractmethod
    def borrow_limit(self):
        ...

    @property
    @abstractmethod
    def role(self):
        ...

    def can_borrow(self):
        return len(self.loans) < self.borrow_limit

    def to_dict(self):
        return {"role": self.role, "id": self.member_id, "name": self.name}

    def __str__(self):
        return f"{self.role} {self.name} ({self.member_id}) - {len(self.loans)}/{self.borrow_limit} items"


class Student(Member):
    role = "Student"
    borrow_limit = 3


class Teacher(Member):
    role = "Teacher"
    borrow_limit = 6
    FINE_PER_DAY = 5   # teachers get a discount (overriding a class attribute)


# ------------------------------------------------------------------ loan
class Loan:
    def __init__(self, item, member, borrowed_on=None):
        self.item = item
        self.member = member
        self.borrowed_on = borrowed_on or date.today()
        self.due_date = self.borrowed_on + timedelta(days=item.loan_days)

    def fine(self, returned_on=None):
        returned_on = returned_on or date.today()
        late_days = (returned_on - self.due_date).days
        return max(0, late_days) * self.member.FINE_PER_DAY

    def to_dict(self):
        return {"item_id": self.item.item_id, "member_id": self.member.member_id,
                "borrowed_on": self.borrowed_on.isoformat()}
