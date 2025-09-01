
# ---------------- Node Structure ----------------
class BookNode:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available
        self.next = None  # self-referential (linked list)

    def __repr__(self):
        status = "Available" if self.available else "Borrowed"
        return f"📖 {self.title} by {self.author} [{status}]"

# ---------------- E-Library Class ----------------
class ELibrary:
    def __init__(self):
        self.head = None         # Linked list head
        self.undo_stack = []     # Stack for undo actions

    # Add book alphabetically
    def add_book(self, title, author):
        new_node = BookNode(title, author)

        if self.head is None or self.head.title.lower() > title.lower():
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.title.lower() < title.lower():
                current = current.next
            new_node.next = current.next
            current.next = new_node
        print(f"✅ Added book: {title} by {author}")

    # Borrow a book
    def borrow_book(self, title):
        current = self.head
        while current:
            if current.title.lower() == title.lower():
                if current.available:
                    current.available = False
                    self.undo_stack.append(("borrow", current))
                    print(f"📕 You borrowed '{current.title}'")
                else:
                    print("❌ Book already borrowed.")
                return
            current = current.next
        print("❌ Book not found.")

    # Return a book
    def return_book(self, title):
        current = self.head
        while current:
            if current.title.lower() == title.lower():
                if not current.available:
                    current.available = True
                    self.undo_stack.append(("return", current))
                    print(f"📗 You returned '{current.title}'")
                else:
                    print("❌ Book was not borrowed.")
                return
            current = current.next
        print("❌ Book not found.")

    # Undo last action
    def undo(self):
        if not self.undo_stack:
            print("⚠️ No actions to undo.")
            return
        action, book = self.undo_stack.pop()
        if action == "borrow":
            book.available = True
            print(f"↩️ Undo: Returned '{book.title}'")
        elif action == "return":
            book.available = False
            print(f"↩️ Undo: Borrowed '{book.title}'")

    # Search by title or author
    def search(self, keyword):
        current = self.head
        found = False
        while current:
            if keyword.lower() in current.title.lower() or keyword.lower() in current.author.lower():
                print(current)
                found = True
            current = current.next
        if not found:
            print("❌ No matching books found.")

    # Display all books
    def display_books(self):
        if not self.head:
            print("📭 No books in library.")
            return
        current = self.head
        print("\n--- Library Inventory ---")
        while current:
            print(current)
            current = current.next


# ---------------- DEMO ----------------
if __name__ == "__main__":
    library = ELibrary()

    # Add some books
    library.add_book("Python Programming", "Guido van Rossum")
    library.add_book("Data Structures", "Narasimha Karumanchi")
    library.add_book("Clean Code", "Robert C. Martin")

    # Display
    library.display_books()

    # Borrow/Return
    library.borrow_book("Python Programming")
    library.return_book("Python Programming")

    # Undo operations
    library.undo()
    library.undo()

    # Search
    library.search("Code")
    library.search("Narasimha")
