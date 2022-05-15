class Transition:
    def __init__(self, etat_0: str, etat_1: str, lettre: str):
        self.etat_0 = etat_0
        self.etat_1 = etat_1
        self.lettre = lettre

        # Vérifie si les états appartiennent au même automate
        assert self.etat_0.automate == self.etat_1.automate

        self.etat_0.automate.transitions.add(self)
        self.etat_0.transition_0.add(self)
        self.etat_1.transition_1.add(self)

    def copy(self, automate: object = None) -> object:
        if automate is None:
            automate = self.automate

        copieEtat_0 = automate.getEtat(self.etat_0.numeroEtat)
        copieEtat_1 = automate.getEtat(self.etat_1.numeroEtat)
        copieLettre = automate.alphabet.getLettre(self.lettre.caractere)

        return Transition(copieEtat_0, copieEtat_1, copieLettre)

    def remove(self) -> object:
        self.etat_0.automate.transitions.remove(self)
        self.etat_0.transition_0.remove(self)
        self.etat_1.transition_1.remove(self)
