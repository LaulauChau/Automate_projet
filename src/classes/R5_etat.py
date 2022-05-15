class Etat:
    def __init__(
        self,
        automate: object,
        numeroEtat: str,
        initial: bool = False,
        terminal: bool = False,
    ):
        self.automate = automate
        self.numeroEtat = numeroEtat
        self.transition_0 = set()  # transitions entrantes
        self.transition_1 = set()  # transitions sortantes
        self.initial = initial
        self.terminal = terminal
        self.automate.etats.add(self)

        if initial:
            self.automate.etatsInitiaux.add(self)
        if terminal:
            self.automate.etatsTerminaux.add(self)

    def copy(self, automate: object) -> object:
        if automate is None:
            automate = self.automate

        return Etat(automate, self.numeroEtat, self.initial, self.terminal)

    def remove(self) -> None:
        for transition in self.transition_0.copy():
            transition.remove()

        for transition in self.transition_1.copy():
            transition.remove()

        self.automate.etats.remove(self)

        if self.initial:
            self.automate.etatsInitiaux.remove(self)
        if self.terminal:
            self.automate.etatsTerminaux.remove(self)

    def getNextEtat(self, lettre: str) -> object:
        return {
            transition.etat_1
            for transition in self.transition_0
            if transition.lettre == lettre
        }

    def getPreviousEtat(self, lettre: str) -> object:
        return {
            transition.etat_0
            for transition in self.transition_1
            if transition.lettre == lettre
        }
