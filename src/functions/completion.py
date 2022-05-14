from src.classes.etat import Etat
from src.classes.transition import Transition
from src.functions.determinisation import determinize
from src.functions.synchronisation import synchronize


def completer(automate, file=None):
    automate = synchronize(automate, file=file)

    if automate.checkComplet(file=file):
        return automate

    etatPoubelle = Etat(automate, "P")

    for etat in automate.etats:
        transitionSortante = {
            transition.lettre for transition in etat.transition_0.copy()
        }

        for lettre in set(automate.alphabet.lettres) - transitionSortante:
            if not lettre.epsilon:
                Transition(etat, etatPoubelle, lettre)

    return automate


def complement(automate, file=None):
    automate = completer(determinize(automate, file=file), file=file).copy()

    for etat in automate.etats:
        etat.terminal = not etat.terminal

        if etat.terminal:
            automate.etatsTerminaux.add(etat)
        else:
            automate.etatsTerminaux.remove(etat)

    return automate
