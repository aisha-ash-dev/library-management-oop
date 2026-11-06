class LibraryError(Exception):
    """Base class for all library errors."""

class ItemNotFound(LibraryError): pass
class MemberNotFound(LibraryError): pass
class ItemUnavailable(LibraryError): pass
class BorrowLimitReached(LibraryError): pass
