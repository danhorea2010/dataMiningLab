class PlayerStats:
    blitz_rating: int
    bullet_rating: int
    rapid_rating: int

    def __init__(self, rapid_rating: int, bullet_rating: int, blitz_rating: int):
        self.rapid_rating = rapid_rating
        self.bullet_rating = bullet_rating
        self.blitz_rating = blitz_rating