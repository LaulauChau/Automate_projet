import re

from src.classes.alphabet import Alphabet
from src.classes.etat import Etat
from src.classes.lettre import Lettre
from src.classes.transition import Transition

LETTRES = "abcdefghijklmnopqrstuvwxyz"
ETATS = list(map(str, range(100)))


class Automate:
    def __init__(
        self,
        alphabet=None,
        etats=None,
        transitions=None,
        etatsInitiaux=None,
        etatsTerminaux=None,
    ):
        self.alphabet = alphabet if alphabet is not None else Alphabet()
        self.etats = etats if etats is not None else set()
        self.transitions = transitions if transitions is not None else set()
        self.etatsInitiaux = etatsInitiaux if etatsInitiaux is not None else set()
        self.etatsTerminaux = etatsTerminaux if etatsTerminaux is not None else set()

    def copy(self, alphabet=None):
        if alphabet is None:
            alphabet = self.alphabet

        copieAutomate = Automate(alphabet)

        for etat in self.etats:
            etat.copy(copieAutomate)

        for transition in self.transitions:
            transition.copy(copieAutomate)

        return copieAutomate

    def getEtat(self, numeroEtat):
        return next(
            (etat for etat in self.etats if etat.numeroEtat == numeroEtat), None
        )

    def checkAsynchrone(self, file=None):
        for transition in sorted(
            self.transitions,
            key=lambda transition: (
                transition.etat_0.numeroEtat,
                transition.etat_1.numeroEtat,
                transition.lettre.caractere,
            ),
        ):
            if transition.lettre.epsilon:
                print(
                    f"Cet automate est asynchrone car il a au moins une transition epsilon ({transition.etat_0.numeroEtat}{transition.lettre.caractere}{transition.etat_1.numeroEtat})."
                )
                return True

            print("Cet automate est déjà synchrone.", file=file)
            return False

    def checkDeterministe(self, file=None):
        if len(self.etatsInitiaux) > 1:
            print(
                f"Cet automate n'est pas déterministe car il possède {len(self.etatsInitiaux)} états initiaux.",
                file=file,
            )
            return False

        association = set()

        for transition in sorted(
            self.transitions,
            key=lambda transition: (
                transition.etat_0.numeroEtat,
                transition.etat_1.numeroEtat,
                transition.lettre.caractere,
            ),
        ):
            membre = (transition.etat_0, transition.lettre)

            if membre in association:
                print(
                    f"Cet automate n'est pas déterministe car il a plusieurs transitions qui partent du même état ({transition.etat_0.numeroEtat}) avec la lettre ({transition.lettre.caractere}).",
                    file=file,
                )
                return False

            association.add(membre)

        print("Cet automate est déjà déterministe.", file=file)
        return True

    def checkComplet(self, file=None):
        association = set()

        for transition in self.transitions:
            if transition.lettre.epsilon:
                print(
                    "Cet automate ne peut pas être complété car il est asynchrone.",
                    file=file,
                )
                return False

            association.add((transition.etat_0, transition.lettre))

        cpt = sum(not lettre.epsilon for lettre in self.alphabet.lettres)

        if len(association) >= len(self.etats) * cpt:
            print("Cet automate est déjà completé.", file=file)
            return True
        else:
            print(
                f"Cet automate est incomplet car il manque {(len(self.etats) * cpt - len(association))} transition(s).",
                file=file,
            )
            return False

    def checkStandard(self, file=None):
        if len(self.etatsInitiaux) > 1:
            print(
                f"Cet automate n'est pas standard car il a {len(self.etatsInitiaux)} états initiaux.",
                file=file,
            )
            return False

        etatInitial = next(iter(self.etatsInitiaux))

        for transition in sorted(
            self.transitions,
            key=lambda transition: (
                transition.etat_0.numeroEtat,
                transition.etat_1.numeroEtat,
                transition.lettre.caractere,
            ),
        ):
            if transition.etat_1 == etatInitial:
                print(
                    f"Cet automate n'est pas standard car il présente au moins une transition qui revient vers l'état initial ({transition.etat_0.numeroEtat}{transition.lettre.caractere}{transition.etat_1.numeroEtat}).",
                    file=file,
                )
                return False

        print("Cet automate est déjà standard.", file=file)
        return True

    def display(self, file=None):
        lettres = [
            lettre.caractere for lettre in self.alphabet.lettres if not lettre.epsilon
        ]
        lettres.sort()
        print("Alphabet : ", *lettres, file=file)

        etatsInitiaux = [etat.numeroEtat for etat in self.etatsInitiaux]
        etatsInitiaux.sort()
        print("Etats initiaux : ", *etatsInitiaux, file=file)

        etatsTerminaux = [etat.numeroEtat for etat in self.etatsTerminaux]
        etatsTerminaux.sort()
        print("Etats terminaux : ", *etatsTerminaux, file=file)

        print("Table de transition :", file=file)

        lettres = []
        for lettre in self.alphabet.lettres:
            for transition in self.transitions:
                if transition.lettre == lettre:
                    lettres.append(lettre)
                    break

        largeurColonnes = [0] * (len(lettres) + 1)
        for i, lettre in enumerate(
            sorted(lettres, key=lambda lettre: lettre.caractere)
        ):
            largeurColonnes[i + 1] = max(largeurColonnes[i + 1], len(lettre.caractere))

        for etat in sorted(self.etats, key=lambda etat: etat.numeroEtat):
            largeurColonne = len(etat.numeroEtat)

            if etat.initial or etat.terminal:
                largeurColonne += 1
            if etat.initial:
                largeurColonne += 1
            if etat.terminal:
                largeurColonne += 1

            largeurColonnes[0] = max(largeurColonnes[0], largeurColonne)
            for i, lettre in enumerate(
                sorted(lettres, key=lambda lettre: lettre.caractere)
            ):
                etatSuivant = etat.getNextEtat(lettre)
                largeurColonne = (
                    sum(map(lambda etat: len(etat.numeroEtat), etatSuivant))
                    + len(etatSuivant)
                    - 1
                )
                largeurColonnes[i + 1] = max(largeurColonnes[i + 1], largeurColonne)

        print("/".center(largeurColonnes[0] + 2), end="", file=file)
        for i, lettre in enumerate(
            sorted(lettres, key=lambda lettre: lettre.caractere)
        ):
            print(
                f"|{lettre.caractere.center(largeurColonnes[i + 1] + 2)}",
                end="",
                file=file,
            )
        print(file=file)
        print("-" * (largeurColonnes[0] + 2), end="", file=file)
        for i in range(len(lettres)):
            print("+" + "-" * (largeurColonnes[i + 1] + 2), end="", file=file)
        print(file=file)

        for etat in sorted(self.etats, key=lambda etat: etat.numeroEtat):
            enTete = etat.numeroEtat

            if etat.initial or etat.terminal:
                enTete = f" {enTete}"
            if etat.initial:
                enTete = f"→{enTete}"
            if etat.terminal:
                enTete = f"←{enTete}"

            print(enTete.center(largeurColonnes[0] + 2), end="", file=file)

            for i, lettre in enumerate(
                sorted(lettres, key=lambda lettre: lettre.caractere)
            ):
                etatSuivant = etat.getNextEtat(lettre)
                etatSuivant = " ".join(
                    sorted(map(lambda etat: etat.numeroEtat, etatSuivant))
                )
                print(
                    f"|{etatSuivant.center(largeurColonnes[i + 1] + 2)}",
                    end="",
                    file=file,
                )
            print(file=file)

    def readFile(
        file=None,
    ):  # sourcery skip: instance-method-first-arg-name, raise-specific-error
        with open(file) as f:
            longueurAlphabet = int(f.readline())
            compteurEtats = int(f.readline())

            nombreEtatsInitiaux = f.readline().split()
            compteurEtatsInitiaux = nombreEtatsInitiaux[0]
            nombreEtatsInitiaux = set(nombreEtatsInitiaux[1:])

            nombreEtatsTerminaux = f.readline().split()
            compteurEtatsTerminaux = nombreEtatsTerminaux[0]
            nombreEtatsTerminaux = set(nombreEtatsTerminaux[1:])

            compteurTransition = int(f.readline())
            transitionDescription = [f.readline() for _ in range(compteurTransition)]
        alphabet = Alphabet()
        for caractere in LETTRES[:longueurAlphabet]:
            Lettre(alphabet, caractere)
        Lettre(alphabet, epsilon=True)

        automate = Automate(alphabet)

        for numeroEtat in ETATS[:compteurEtats]:
            initial = numeroEtat in nombreEtatsInitiaux
            terminal = numeroEtat in nombreEtatsTerminaux
            Etat(automate, numeroEtat, initial=initial, terminal=terminal)

        for transitionDesc in transitionDescription:
            if match := re.match(r"^(\d+)(\D+)(\d+)\n?$", transitionDesc):
                iDEtat_0 = match[1]
                caractere = match[2]
                iDEtat_1 = match[3]

                etat_0 = automate.getEtat(iDEtat_0)
                etat_1 = automate.getEtat(iDEtat_1)
                lettre = alphabet.getLettre(caractere)

                Transition(etat_0, etat_1, lettre)
            else:
                raise Exception("Format invalide.")

        return automate
