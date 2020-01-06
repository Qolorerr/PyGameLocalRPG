class Level:
    def __init__(self, max_exp, coeff):
        self.max_exp = max_exp
        self.coeff = coeff
        self.level = 1
        self.exp = 0

    def add_exp(self, exp):
        self.exp += exp
        while self.exp > self.max_exp:
            self.level += 1
            self.exp -= self.max_exp
            self.max_exp *= self.coeff

    def get(self):
        return self.level