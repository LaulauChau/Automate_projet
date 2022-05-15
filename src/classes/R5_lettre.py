class Lettre:
    def __init__(self, alphabet: object, caractere: str = None, epsilon: bool = None):
        self.alphabet = alphabet
        self.epsilon = epsilon if epsilon is not None else (caractere == "*")
        self.caractere = (
            caractere if caractere is not None else "*" if self.epsilon else None
        )
        self.alphabet.lettres.add(self)

    def copy(self, alphabet: object = None) -> object:
        if alphabet is None:
            alphabet = self.alphabet

        return Lettre(alphabet, self.caractere, self.epsilon)
