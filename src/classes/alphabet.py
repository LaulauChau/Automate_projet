class Alphabet:
    def __init__(self, lettres=None):
        self.lettres = lettres if lettres is not None else set()

    def copy(self):
        copieAlphabet = Alphabet()

        for lettre in self.lettres:
            lettre.copy(copieAlphabet)

    def getLettre(self, caractere):
        return next(
            (lettre for lettre in self.lettres if lettre.caractere == caractere), None
        )
