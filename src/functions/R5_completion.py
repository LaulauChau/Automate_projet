from src.classes.R5_etat import Etat
from src.classes.R5_transition import Transition
from src.functions.R5_determinisation import determinize
from src.functions.R5_synchronisation import synchronize


def completer(automate: object, file=None) -> object:
    automate = synchronize(automate, file=file)

    if automate.checkComplet(file=file):
        return automate

    etatPoubelle = Etat(automate, "P")

    for etat in automate.etats:
        # Pour chaque état, trouver les lettres qui n'ont pas de transitions sortantes
        transitionSortante = {
            transition.lettre for transition in etat.transition_0.copy()
        }

        # Ajoute une transition vers l'état poubelle
        for lettre in set(automate.alphabet.lettres) - transitionSortante:
            if not lettre.epsilon:
                Transition(etat, etatPoubelle, lettre)

    return automate


def complement(automate: object, file=None) -> object:
    automate = completer(determinize(automate, file=file), file=file).copy()

    for etat in automate.etats:
        # Inverse les états terminaux et non terminaux
        etat.terminal = not etat.terminal

        if etat.terminal:
            automate.etatsTerminaux.add(etat)
        else:
            automate.etatsTerminaux.remove(etat)

    return automate
