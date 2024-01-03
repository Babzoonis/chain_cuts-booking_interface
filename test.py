def calculate_chain_cuts(koll_zvenyev):
    spisok = [1.0]
    mesta_razrezov = []
    element = 0

    while koll_zvenyev - 1 != 0:
        if koll_zvenyev % 2 != 0:
            element = koll_zvenyev - ((koll_zvenyev - 1) / 2)
            koll_zvenyev = (koll_zvenyev - 1) / 2
        else:
            element = koll_zvenyev / 2


            koll_zvenyev = koll_zvenyev / 2
        mesta_razrezov += [koll_zvenyev]
        spisok += [element]

    spisok.sort()

    return len(spisok) - 2, spisok, mesta_razrezov[:-1]
