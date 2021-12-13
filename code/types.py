from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self == other


@dataclass
class Field:
    p: int  # prime modulus
    q: int  # order of the base point
    h: int = 1


@dataclass
class EllipticCurve:
    a: int  # coefficient
    b: int  # coefficient
    base: Point  # base point
    field: Field
    inf: Point = Point(0, 0)  # point of infinity
    name: str = "undefined"


@dataclass
class KeyPair:
    public: Point
    private: int


@dataclass
class SharedKey:
    key: Point
    sharedWith: str

    def __str__(self):
        return f"shared with: {self.sharedWith}, key: {self.key}\n"


@dataclass
class KeyManager:
    ownKeys: KeyPair
    shared: list  # list of shared keys
    size: int
    id: str = ""

    def __str__(self):
        return f'--- KEY MANAGER ---\nowner: {self.id} \nkeys size: {self.size} \npublic key: {self.ownKeys.public} \nprivate: {self.ownKeys.private} \nshared keys: \n{"".join(["".join(["  # ", str(sh)]) for sh in self.shared])}'
