class Item:
    def __init__(self, name: str, url: str, price_old: float | None, price_new: float) -> None:
        self.name = name
        self.url = url
        self.price_old = price_old
        self.price_new = price_new

    def __repr__(self) -> str:
        return f"name: {self.name} price_old: {self.price_old} price_new: {self.price_new} url: {self.url}"