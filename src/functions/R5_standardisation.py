from src.classes.R5_etat import Etat
from src.classes.R5_transition import Transition


def standardize(automate: object, file=None) -> object:
    automate = automate.copy()

    if automate.checkStandard(file=file):
        return automate

    # Création nouvel état initial
    etatInitial = Etat(automate, "I", initial=True)

    for etat in automate.etatsInitiaux.copy():
        if etat == etatInitial:
            continue

        # Reset la liste des états initiaux
        etat.initial = False
        automate.etatsInitiaux.remove(etat)

        # Copie les transitions des états initiaux de base vers le nouvel état initial
        association = set()
        for transition in etat.transition_0:
            membre = (transition.etat_1, transition.lettre)

            if membre in association:
                continue

            Transition(etatInitial, transition.etat_1, transition.lettre)
            association.add(membre)

    return automate
