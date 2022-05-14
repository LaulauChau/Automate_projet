from src.classes.R5_etat import Etat
from src.classes.R5_transition import Transition


def standardize(automate, file=None):
    automate = automate.copy()

    if automate.checkStandard(file=file):
        return automate

    etatInitial = Etat(automate, "I", initial=True)

    for etat in automate.etatsInitiaux.copy():
        if etat == etatInitial:
            continue

        etat.initial = False
        automate.etatsInitiaux.remove(etat)

        association = set()
        for transition in etat.transition_0:
            membre = (transition.etat_1, transition.lettre)

            if membre in association:
                continue

            Transition(etatInitial, transition.etat_1, transition.lettre)
            association.add(membre)

    return automate
