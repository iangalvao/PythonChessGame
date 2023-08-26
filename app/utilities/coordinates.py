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

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return "Coordinate " + self.__str__()

    def __mul__(self, other):
        assert isinstance(other, int)
        return Coordinate(self.x * other, self.y * other)

    def __rmul__(self, other):
        assert isinstance(other, int)
        return Coordinate(self.x * other, self.y * other)
