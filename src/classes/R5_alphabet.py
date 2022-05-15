class Alphabet:
    def __init__(self, lettres=None):
        # Initialise l'object avec les lettres reconnus par l'alphabet de l'automate
        self.lettres = lettres if lettres is not None else set()

    def copy(self) -> None:
        copieAlphabet = Alphabet()

        for lettre in self.lettres:
            lettre.copy(copieAlphabet)

    def getLettre(self, caractere: str) -> str:
        return next(
            (lettre for lettre in self.lettres if lettre.caractere == caractere), None
        )
