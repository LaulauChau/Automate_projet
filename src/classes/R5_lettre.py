class Lettre:
    def __init__(self, alphabet, caractere=None, epsilon=None):
        self.alphabet = alphabet
        self.epsilon = epsilon if epsilon is not None else (caractere == "*")
        self.caractere = (
            caractere if caractere is not None else "*" if self.epsilon else None
        )
        self.alphabet.lettres.add(self)

    def copy(self, alphabet=None):
        if alphabet is None:
            alphabet = self.alphabet

        return Lettre(alphabet, self.caractere, self.epsilon)
