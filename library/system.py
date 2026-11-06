"""Library: the controller class that ties items, members and loans together."""
import json
from datetime import date

from .exceptions import (BorrowLimitReached, ItemNotFound, ItemUnavailable,
                         MemberNotFound)
from .models import DVD, Book, Loan, Magazine, Student, Teacher

MEMBER_TYPES = {"Student": Student, "Teacher": Teacher}


class Library:
    def __init__(self):
        self.items = {}
        self.members = {}

    # ---- management
    def add_item(self, item):
        self.items[item.item_id] = item

    def add_member(self, member):
        self.members[member.member_id] = member

    def _get_item(self, item_id):
        if item_id not in self.items:
            raise ItemNotFound(f"No item with id {item_id}")
        return self.items[item_id]

    def _get_member(self, member_id):
        if member_id not in self.members:
            raise MemberNotFound(f"No member with id {member_id}")
        return self.members[member_id]

    # ---- operations
    def borrow(self, member_id, item_id, today=None):
        member, item = self._get_member(member_id), self._get_item(item_id)
        if not member.can_borrow():
            raise BorrowLimitReached(f"{member.name} reached the limit of {member.borrow_limit}")
        if not item.checkout():
            raise ItemUnavailable(f"'{item.title}' has no copies left")
        loan = Loan(item, member, today)
        member.loans.append(loan)
        return loan

    def give_back(self, member_id, item_id, today=None):
        """Return an item. Gives back the fine amount (0 if on time)."""
        member = self._get_member(member_id)
        for loan in member.loans:
            if loan.item.item_id == item_id:
                member.loans.remove(loan)
                loan.item.give_back()
                return loan.fine(today)
        raise ItemNotFound(f"{member.name} has not borrowed {item_id}")

    def search(self, text):
        text = text.lower()
        return [i for i in self.items.values() if text in i.details().lower()]

    def overdue(self, today=None):
        today = today or date.today()
        return [l for m in self.members.values() for l in m.loans if l.due_date < today]

    # ---- persistence (JSON)
    def save(self, path):
        data = {
            "items": [i.to_dict() for i in self.items.values()],
            "members": [m.to_dict() for m in self.members.values()],
            "loans": [l.to_dict() for m in self.members.values() for l in m.loans],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        lib = cls()
        for d in data["items"]:
            if d["kind"] == "Book":
                item = Book(d["id"], d["title"], d["author"], d["total"])
            elif d["kind"] == "Magazine":
                item = Magazine(d["id"], d["title"], d["issue"], d["total"])
            else:
                item = DVD(d["id"], d["title"], d["minutes"], d["total"])
            lib.add_item(item)
        for d in data["members"]:
            lib.add_member(MEMBER_TYPES[d["role"]](d["id"], d["name"]))
        for d in data["loans"]:
            lib.borrow(d["member_id"], d["item_id"], date.fromisoformat(d["borrowed_on"]))
        return lib
