from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, List


# -----------------------------
# Core Data Model
# -----------------------------
@dataclass
class Station:
    name: str
    minutes_to_next: int = 0  # travel time to NEXT station (used for ETA)


class Node:
    def __init__(self, station: Station):
        self.station: Station = station
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.station.name})"


# -----------------------------
# Doubly Linked (Linear) Route
# -----------------------------
class DoublyLinkedRoute:
    """Linear route: HEAD <---> ... <---> TAIL (no wrapping)."""

    def __init__(self, stations: Optional[Iterable[Station]] = None):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        if stations:
            for st in stations:
                self.append(st)

    def append(self, station: Station) -> Node:
        node = Node(station)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        return node

    def find(self, name: str) -> Optional[Node]:
        cur = self.head
        name_l = name.lower()
        while cur:
            if cur.station.name.lower() == name_l:
                return cur
            cur = cur.next
        return None

    def insert_after(self, anchor: Node, station: Station) -> Node:
        node = Node(station)
        nxt = anchor.next
        anchor.next = node
        node.prev = anchor
        node.next = nxt
        if nxt:
            nxt.prev = node
        else:
            self.tail = node
        return node

    def remove(self, node: Node) -> None:
        if node.prev:
            node.prev.next = node.next
        else:
            # removing head
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            # removing tail
            self.tail = node.prev
        node.prev = node.next = None

    def iter_forward(self) -> Iterable[Node]:
        cur = self.head
        while cur:
            yield cur
            cur = cur.next

    def iter_backward(self) -> Iterable[Node]:
        cur = self.tail
        while cur:
            yield cur
            cur = cur.prev

    def visualize(self) -> str:
        names = []
        cur = self.head
        while cur:
            arrow = " <-> " if cur.next else ""
            names.append(cur.station.name + arrow)
            cur = cur.next
        return "".join(names)


# -----------------------------
# Circular Doubly Linked Route
# -----------------------------
class CircularRoute:
    """Loop route: circular doubly linked list (wraps around)."""

    def __init__(self, stations: Optional[Iterable[Station]] = None):
        self.head: Optional[Node] = None
        self._size = 0
        if stations:
            for st in stations:
                self.append(st)

    def append(self, station: Station) -> Node:
        node = Node(station)
        if self.head is None:
            # first node points to itself
            node.next = node.prev = node
            self.head = node
        else:
            tail = self.head.prev  # type: ignore
            # insert between tail and head
            node.prev = tail
            node.next = self.head
            tail.next = node
            self.head.prev = node
        self._size += 1
        return node

    def find(self, name: str) -> Optional[Node]:
        if self.head is None:
            return None
        name_l = name.lower()
        cur = self.head
        for _ in range(self._size):
            if cur.station.name.lower() == name_l:
                return cur
            cur = cur.next  # type: ignore
        return None

    def insert_after(self, anchor: Node, station: Station) -> Node:
        node = Node(station)
        nxt = anchor.next
        anchor.next = node
        node.prev = anchor
        node.next = nxt
        nxt.prev = node  # type: ignore
        self._size += 1
        return node

    def remove(self, node: Node) -> None:
        if self.head is None:
            return
        if self._size == 1 and node is self.head:
            self.head = None
            self._size = 0
            node.prev = node.next = None
            return

        node.prev.next = node.next  # type: ignore
        node.next.prev = node.prev  # type: ignore
        if node is self.head:
            self.head = node.next
        node.prev = node.next = None
        self._size -= 1

    def iter_once(self) -> Iterable[Node]:
        if self.head is None:
            return
        cur = self.head
        for _ in range(self._size):
            yield cur
            cur = cur.next  # type: ignore

    def size(self) -> int:
        return self._size

    def visualize(self) -> str:
        if self.head is None:
            return "(empty)"
        names: List[str] = []
        for node in self.iter_once():
            names.append(node.station.name)
        return " <-> ".join(names) + "  (loops)"


# -----------------------------
# Cursor / Navigation
# -----------------------------
class TrainCursor:
    """
    Cursor that moves along a route (linear or circular).
    Supports:
      - current(), next(), prev()
      - jump_to(station_name)
      - eta_to(target_name)
    """

    def __init__(self, route, start: Optional[str] = None):
        self.route = route
        self.current_node: Optional[Node] = None

        # choose start
        if isinstance(route, DoublyLinkedRoute):
            self.current_node = route.head
            if start:
                found = route.find(start)
                if found:
                    self.current_node = found
        elif isinstance(route, CircularRoute):
            self.current_node = route.head
            if start:
                found = route.find(start)
                if found:
                    self.current_node = found
        else:
            raise TypeError("Unsupported route type")

    # ---- Navigation ----
    def current(self) -> Optional[Station]:
        return self.current_node.station if self.current_node else None

    def next(self, steps: int = 1) -> Optional[Station]:
        if not self.current_node:
            return None
        for _ in range(steps):
            nxt = self.current_node.next
            if nxt is None:
                # End of linear route
                return self.current()
            self.current_node = nxt
        return self.current()

    def prev(self, steps: int = 1) -> Optional[Station]:
        if not self.current_node:
            return None
        for _ in range(steps):
            prv = self.current_node.prev
            if prv is None:
                # Start of linear route
                return self.current()
            self.current_node = prv
        return self.current()

    def jump_to(self, name: str) -> bool:
        found = self.route.find(name)
        if found:
            self.current_node = found
            return True
        return False

    # ---- ETA (simple) ----
    def eta_to(self, target_name: str) -> Optional[int]:
        """
        Sum minutes_to_next along the path from current to target (forward direction).
        For linear route, stops at end if target not reachable ahead.
        For circular route, wraps as needed (but will stop after one full loop if not found).
        """
        if not self.current_node:
            return None

        # Circular detection:
        is_circular = isinstance(self.route, CircularRoute)

        cur = self.current_node
        minutes = 0
        visited = 0
        limit = self.route.size() if is_circular else 10**9  # safe cap

        while True:
            if cur.station.name.lower() == target_name.lower():
                return minutes

            nxt = cur.next
            if nxt is None:
                # linear end reached
                return None

            minutes += cur.station.minutes_to_next
            cur = nxt

            if not is_circular and cur is None:
                return None

            visited += 1
            if is_circular and visited > limit:
                # Not found in a full loop
                return None


# -----------------------------
# Demo / Quick Test
# -----------------------------
if __name__ == "__main__":
    # Linear route (Doubly Linked)
    print("=== Linear Route ===")
    linear = DoublyLinkedRoute(
        [
            Station("Alpha", minutes_to_next=3),
            Station("Bravo", minutes_to_next=5),
            Station("Charlie", minutes_to_next=2),
            Station("Delta", minutes_to_next=4),
        ]
    )
    print("Map:", linear.visualize())

    cursor = TrainCursor(linear, start="Bravo")
    print("Start at:", cursor.current())
    cursor.next()
    print("After next():", cursor.current())
    cursor.prev()
    print("After prev():", cursor.current())
    print("ETA Bravo -> Delta:", cursor.eta_to("Delta"), "min")
    # insert Echo after Charlie
    ch = linear.find("Charlie")
    if ch:
        linear.insert_after(ch, Station("Echo", minutes_to_next=6))
    print("Map (after insert):", linear.visualize())

    # Circular route (Loop)
    print("\n=== Circular Loop Route ===")
    loop = CircularRoute(
        [
            Station("North", minutes_to_next=4),
            Station("East", minutes_to_next=3),
            Station("South", minutes_to_next=5),
            Station("West", minutes_to_next=2),
        ]
    )
    print("Map:", loop.visualize())

    loop_cursor = TrainCursor(loop, start="West")
    print("Start at:", loop_cursor.current())
    loop_cursor.next()  # wraps to North
    print("After next() (wrap):", loop_cursor.current())
    loop_cursor.prev()  # back to West
    print("After prev() (wrap):", loop_cursor.current())
    print("ETA West -> South:", loop_cursor.eta_to("South"), "min")

    # Remove a station from loop
    node_south = loop.find("South")
    if node_south:
        loop.remove(node_south)
    print("Map (after removing South):", loop.visualize())