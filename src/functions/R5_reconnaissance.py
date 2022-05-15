def impasse(etat: object, parents: set = None) -> bool:
    if parents is None:
        parents = set()
    elif etat in parents:
        return True

    # Si on trouve un état terminal, ce n'est pas une impasse
    if etat.terminal:
        return False

    # Vérifie chaque transitions sortantes
    # Si elles sont toutes des impasses, cet état est une impasse aussi
    return not any(
        transition.etat_1 not in parents
        and not impasse(transition.etat_1, parents=parents.union({etat}))
        for transition in etat.transition_0
    )


def reconnaissance(automate: object) -> None:
    while True:
        mot = input(
            "Entrez le mot à tester (ou suivant/s pour passer à l'étape suivante) : "
        )

        # Permet à l'utilisateur de quitter
        if mot.lower() in ["suivant", "s"]:
            break

        # Démarre avec l'état initial
        etatsActifs = automate.etatsInitiaux

        for i, caractere in enumerate(mot):
            lettre = automate.alphabet.getLettre(caractere)

            # Vérifie si la lettre est dans l'alphabet de l'automate
            if lettre is None:
                etatsActifs = set()
                print(f"La lettre {caractere} n'est pas dans l'alphabet.")
                break

            nextEtatsActifs = set()
            for etatActif in etatsActifs:
                for nextEtat in etatActif.getNextEtat(lettre):
                    nextEtatsActifs.add(nextEtat)

            etatsActifs = nextEtatsActifs
            for etatActif in etatsActifs:
                # Si impasse, le mot ne peut pas être reconnu
                if not impasse(etatActif):
                    break
            else:
                print(
                    f"Avec comme caractère initial {mot[:i+1]}, le mot ne peut pas être reconnue par l'automate."
                )
                break
        for etatActif in etatsActifs:
            # Si au moins un etat est terminal, le mot est reconnu
            if etatActif.terminal:
                print(f"Le mot {mot} est reconnue par l'automate.")
                break
        else:
            print(f"Le mot {mot} n'est pas reconnue par l'automate.")
