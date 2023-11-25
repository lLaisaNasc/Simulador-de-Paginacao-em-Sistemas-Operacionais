# -- Ler o arquivo --

doc = open('./arquivos/sc.txt', 'r', encoding='utf8')
algoritmo_substituicao = doc.readline().strip()

# -- Dados do processo --

numero_de_quadros = (eval(doc.readline().strip()))

paginas_processo = [linha.replace('\u00a0', '').strip().split()
                    for linha in doc.readlines() if linha.strip() != ""]

# -- Idenfica o algoritmo de substituição --


def identifica_algoritmo_substituicao(nome_substiuicao, numero_de_quadros, paginas_processo):
    algoritmos = ['FIRST COME FIRST SERVED', 'FIFO',
                  'SC', 'Segunda Chance', '']

    if nome_substiuicao in algoritmos:
        posicao = algoritmos.index(nome_substiuicao)

        if posicao == 0 or posicao == 1:
            utiliza_first_come_first_served(
                numero_de_quadros, paginas_processo)
        elif posicao == 2 or posicao == 3:
            utiliza_segunda_chance(numero_de_quadros, paginas_processo)
        elif posicao == 4:
            ...
    else:
        print('Não foi possível identificar o algoritmo de substituição! :(')

# -- Algoritmo FIFO --


def utiliza_first_come_first_served(numero_de_quadros, paginas_processo):
    fila = []
    page_faults = 0
    page_hits = 0

    print(paginas_processo)

    for operacao in paginas_processo:
        pagina = (eval(operacao[0]))
        if pagina not in fila:
            # -- Se a página não estiver na fila, é um page fault --
            page_faults += 1
            print('page fault - página', pagina)

            if len(fila) < numero_de_quadros:
                # -- Se ainda há espaço na fila, a página é adicionada --
                fila.append(pagina)
            else:
                # -- Se a fila estiver cheia, a primeira página é removida, e adiciona a nova página --
                fila.pop(0)
                fila.append(pagina)
        else:
            # -- Se a página já estiver na fila, é um page hit --
            page_hits += 1
            print('page hit - página', pagina)

    print('\nTotal Page Faults: ', page_faults)
    print('Total Page Hits: ', page_hits)

    return fila, page_faults, page_hits

# -- Algoritmo SC --


def utiliza_segunda_chance(numero_de_quadros, paginas_processo):
    fila = []
    page_faults = 0
    page_hits = 0

    print(paginas_processo)

    for operacao in paginas_processo:
        # -- inicializa todas as páginas com bit 0 --
        pagina = [(eval(operacao[0])), 0]

        # -- verifica se a página não está na fila e da um page fault --
        if pagina not in fila:
            page_faults += 1
            print('page fault - página', pagina)

            # -- verifica se há espaço na fila e adiciona a nova página --
            if len(fila) < numero_de_quadros:
                fila.append(pagina)
            else:
                # -- lógica da segunda chance --
                while (fila[0][1] != 0):
                    fila[0][1] = 0
                    segunda_chance = fila.pop(0)
                    fila.append(segunda_chance)

            # -- remove a página mais antiga e adiciona a nova no final da fila --
                fila.pop(0)
                fila.append(pagina)

         # -- se a página já está na fila da um page hit --
        else:
            for p in fila:
                if p[0] == pagina[0]:
                    p[1] = 1  # Atualiza o bit de referência da página na fila
                    page_hits += 1
                    print('page hit - página', p)
                    break

    print('\nTotal Page Faults: ', page_faults)
    print('Total Page Hits: ', page_hits)

    return fila, page_faults, page_hits


identifica_algoritmo_substituicao(
    algoritmo_substituicao, numero_de_quadros, paginas_processo)
