💬 Chat Message History Manager (Python) A simple Chat Message History Manager implemented in Python. This project simulates a chat application where you can send messages, undo/redo actions, and track timestamps.

📌 Overview The Chat Manager allows you to:

Store messages in a queue before sending. Keep a history of sent messages. Undo the last sent message. Redo undone messages. Track timestamps for each sent message. ✨ Features 📥 Queue for Incoming Messages – Manages messages before sending. 📤 Stack for Sent Messages – Keeps a history of sent messages. ↩ Undo Last Message – Remove the most recent message from history. 🔁 Redo Message – Restore the last undone message. ⏱ Timestamps – Every message shows the time it was sent. 📜 View Chat History – Display all messages in order. 🛠 Data Structures Used Queue (deque) → To temporarily hold incoming messages. Stack (list) → To store sent messages. Stack (list) → To manage undo/redo functionality. ▶ How It Runs Clone this repository: git clone https://github.com/your-username/chat-history-manager.git cd chat-history-manager

📚 E-Library Book Management (Python) A simple E-Library Book Management System implemented in Python. This project demonstrates how to borrow, return, search, and undo actions using linked lists and stacks.

📌 Overview The E-Library system maintains an inventory of books stored in a linked list. Users can borrow and return books, and each action is recorded in a stack to support undo functionality. Books can also be searched or filtered by title or author.

✨ Features ➕ Add Books – Insert new books into the library inventory. 📖 Display Books – View all books with their availability status. 📕 Borrow Books – Borrow a book if it is available. 📗 Return Books – Return a borrowed book. ↩ Undo Last Action – Undo the last borrow/return action using a stack. 🔍 Search/Filter – Search books by title or author. 🛠 Data Structures Used Linked List (Self-referential Structure)

Each book is stored as a node (BookNode) with: title author available (availability status) next (pointer to next book node) Stack (Python list)

Used for undo functionality. Stores recent borrow/return actions and allows reverting them. ▶ How It Runs Clone this repository: git clone https://github.com/your-username/elibrary-book-management.git cd elibrary-book-management

🚆 Virtual Train Route Planner (Python) A simple Virtual Train Route Planner implemented in Python. This project simulates navigation between train stations using doubly linked lists and circular linked lists for flexible route planning.

📌 Overview The Train Route Planner allows users to navigate stations forward and backward (using a doubly linked list), and also handles loop routes (using a circular linked list). This mimics real-life train journeys where routes may be linear or circular.

✨ Features ➕ Add Stations – Create train stations dynamically. ⏩ Forward Navigation – Move to the next station. ⏪ Backward Navigation – Move to the previous station. 🔄 Circular Routes – Navigate continuously in looped routes. 📍 Display Current Route – Show available stations in the route. 🛠 Data Structures Used Doubly Linked List

Used for forward/backward navigation in linear routes. Each station node stores: name (station name) prev (previous station) next (next station) Circular Linked List

Used for loop routes where the train keeps cycling through stations. Last station points back to the first station. ▶ How It Runs Clone this repository: git clone https://github.com/your-username/train-route-planner.git cd train-route-planner
