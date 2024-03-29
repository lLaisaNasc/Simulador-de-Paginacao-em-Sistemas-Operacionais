import random
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
                  'SC', 'SEGUNDA CHANCE', 'NOT RECENTLY USED', 'NRU']

    if nome_substiuicao in algoritmos:
        posicao = algoritmos.index(nome_substiuicao)

        if posicao == 0 or posicao == 1:
            utiliza_first_come_first_served(
                numero_de_quadros, paginas_processo)
        elif posicao == 2 or posicao == 3:
            utiliza_second_chance(numero_de_quadros, paginas_processo)
        elif posicao == 4 or posicao == 5:
            utiliza_not_recently_used(numero_de_quadros, paginas_processo)
    else:
        print('Não foi possível identificar o algoritmo de substituição! :(')

# -- Algoritmo FIFO --


def utiliza_first_come_first_served(numero_de_quadros, paginas_processo):
    fila = []
    page_faults = 0
    page_hits = 0

    print('Páginas do processo:', paginas_processo, '\n')

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


def utiliza_second_chance(numero_de_quadros, paginas_processo):
    fila = []
    bit_referencia = {}
    page_faults = 0
    page_hits = 0

    print('\nPáginas do processo:', paginas_processo, '\n')

    for pagina in paginas_processo:
        numero_pagina = int(pagina[0])

        # Verifica se a página não está na fila (page fault)
        if numero_pagina not in fila:
            page_faults += 1
            print('page fault - página', [numero_pagina, 0])

            # Verifica se há espaço na fila e adiciona a nova página
            if len(fila) < numero_de_quadros:
                fila.append(numero_pagina)
                bit_referencia[numero_pagina] = 0
            else:
                # Lógica da segunda chance
                while bit_referencia[fila[0]] != 0:
                    bit_referencia[fila[0]] = 0
                    segunda_chance = fila.pop(0)
                    fila.append(segunda_chance)
                    print('segunda chance: ', [
                          segunda_chance, bit_referencia[segunda_chance]])

                # Remove a página mais antiga e adiciona a nova
                removida = fila.pop(0)
                print('removida: ', [removida, bit_referencia[removida]])
                bit_referencia.pop(removida)
                fila.append(numero_pagina)
                bit_referencia[numero_pagina] = 0

        # Se a página já está na fila (page hit)
        else:
            bit_referencia[numero_pagina] = 1
            page_hits += 1
            print('page hit - página',
                  [numero_pagina, bit_referencia[numero_pagina]])

    print('\nTotal Page Faults:', page_faults)
    print('Total Page Hits:', page_hits, '\n')

    return fila, page_faults, page_hits


def utiliza_not_recently_used(numero_quadros, paginas_processo):
    memoria = []
    page_faults = 0
    page_hits = 0

    # classes de prioridade - referenciada/modificada
    classe0 = [0, 0]
    classe1 = [0, 1]
    classe2 = [1, 0]
    classe3 = [1, 1]

    for operacao in paginas_processo:
        numero_pagina = int(operacao[0])
        classe_pagina = classe0

        pagina = [numero_pagina, classe_pagina]

        if any(pagina[0] == p[0] for p in memoria):
            print(f"\nPage Hit - Página {pagina[0]} - Operação {operacao[1]}")
            page_hits += 1

            memoria = [p for p in memoria if not (pagina[0] == p[0])]

            if pagina[1] == classe0 and operacao[1] == "r":
                memoria.append([numero_pagina, classe2])
            elif pagina[1] == classe0 and operacao[1] == "w":
                memoria.append([numero_pagina, classe1])
            elif pagina[1] == classe1 and operacao[1] == "r":
                memoria.append([numero_pagina, classe3])
            elif pagina[1] == classe2 and operacao[1] == "w":
                memoria.append([numero_pagina, classe3])

            print(f"Memória = {memoria}")
        else:
            print(f"\nPage Fault - Página {pagina[0]}")
            page_faults += 1

            if len(memoria) < numero_quadros:
                memoria.append(pagina)
                print(f"Memória {memoria}")
            else:
                # páginas por classe
                paginas_classe0 = [p for p in memoria if p[1] == classe0]
                paginas_classe1 = [p for p in memoria if p[1] == classe1]
                paginas_classe2 = [p for p in memoria if p[1] == classe2]
                paginas_classe3 = [p for p in memoria if p[1] == classe3]

                if len(paginas_classe0) > 0:
                    pagina_substituir = random.choice(paginas_classe0)
                elif len(paginas_classe1) > 0:
                    pagina_substituir = random.choice(paginas_classe1)
                elif len(paginas_classe2) > 0:
                    pagina_substituir = random.choice(paginas_classe2)
                elif len(paginas_classe3) > 0:
                    pagina_substituir = random.choice(paginas_classe3)

                print(
                    f"Substituindo página {pagina_substituir[0]} pela página {pagina[0]}")
                memoria.remove(pagina_substituir)
                memoria.append(pagina)

                print(f"Memória = {memoria}")

    print('\nTotal Page Faults: ', page_faults)
    print('Total Page Hits: ', page_hits)


identifica_algoritmo_substituicao(
    algoritmo_substituicao.upper(), numero_de_quadros, paginas_processo)
