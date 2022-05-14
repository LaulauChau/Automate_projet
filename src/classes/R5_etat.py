class Etat:
    def __init__(self, automate, numeroEtat, initial=False, terminal=False):
        self.automate = automate
        self.numeroEtat = numeroEtat
        self.transition_0 = set()
        self.transition_1 = set()
        self.initial = initial
        self.terminal = terminal
        self.automate.etats.add(self)

        if initial:
            self.automate.etatsInitiaux.add(self)
        if terminal:
            self.automate.etatsTerminaux.add(self)

    def copy(self, automate):
        if automate is None:
            automate = self.automate

        return Etat(automate, self.numeroEtat, self.initial, self.terminal)

    def remove(self):
        for transition in self.transition_0.copy():
            transition.remove()

        for transition in self.transition_1.copy():
            transition.remove()

        self.automate.etats.remove(self)

        if self.initial:
            self.automate.etatsInitiaux.remove(self)
        if self.terminal:
            self.automate.etatsTerminaux.remove(self)

    def getNextEtat(self, lettre):
        return {
            transition.etat_1
            for transition in self.transition_0
            if transition.lettre == lettre
        }

    def getPreviousEtat(self, lettre):
        return {
            transition.etat_0
            for transition in self.transition_1
            if transition.lettre == lettre
        }
