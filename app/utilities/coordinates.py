class Coordinate:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        if self.x == other.x:
            if self.y == other.y:
                return True
        return False
