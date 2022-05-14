from src.classes.R5_automate import Automate
from src.classes.R5_etat import Etat
from src.classes.R5_transition import Transition
from src.functions.R5_synchronisation import synchronize


def determinize(automate, file=None):
    automate = synchronize(automate, file=file)

    if automate.checkDeterministe(file=file):
        return automate

    automateDeterminiser = Automate(automate.alphabet)
    pourTraitement = [(None, None, automate.etatsInitiaux)]

    while pourTraitement:
        depuisEtat, depuisLettre, traitement = pourTraitement.pop(0)
        numeroNouveauEtat = ",".join(
            sorted(map(lambda etat: etat.numeroEtat, traitement))
        )

        nouvEtat = automateDeterminiser.getEtat(numeroNouveauEtat)
        traiter = True
        if nouvEtat is None:
            traiter = False
            nouvEtat = Etat(automateDeterminiser, numeroNouveauEtat)

        if depuisEtat is not None and depuisLettre is not None:
            Transition(depuisEtat, nouvEtat, depuisLettre)
        else:
            nouvEtat.initial = True
            automateDeterminiser.etatsInitiaux.add(nouvEtat)

        if traiter:
            continue

        nouvTransition = {}
        for etat in traitement:
            if etat.terminal:
                nouvEtat.terminal = True
                automateDeterminiser.etatsTerminaux.add(nouvEtat)

            for transition in etat.transition_0:
                if transition.lettre not in nouvTransition:
                    nouvTransition[transition.lettre] = set()

                nouvTransition[transition.lettre].add(transition.etat_1)

        pourTraitement.extend(
            (nouvEtat, lettre, etatSuiv) for lettre, etatSuiv in nouvTransition.items()
        )

    return automateDeterminiser
