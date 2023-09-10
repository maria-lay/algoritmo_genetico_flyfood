from typing import List, Callable
import random
from math import cos, radians
import time


def gerar_populacao_inicial(lista: List[list], numero_individuo: int) -> List[List[list]]:
    # Verifica se a lista de entrada está vazia ou se é desejado apenas um indivíduo.
    if len(lista) <= 1 or numero_individuo == 1:
        # Retorna uma lista contendo a lista de entrada como único indivíduo.
        return [lista]

    # Inicializa uma lista vazia para armazenar as populações geradas.
    lista_aux = []

    # Itera sobre os elementos na lista de entrada.
    for i, atual in enumerate(lista):
        # Cria uma lista de elementos restantes, excluindo o elemento atual.
        elementos_restantes = lista[:i] + lista[i + 1:]

        # Chama a função recursivamente com os elementos restantes.
        for p in gerar_populacao_inicial(elementos_restantes, numero_individuo):
            # Concatena o elemento atual com a população gerada.
            lista_aux.append([atual] + p)

            # Verifica se o tamanho da população desejada foi alcançado.
            if len(lista_aux) == numero_individuo:
                # Embaralha a ordem dos indivíduos para aumentar a diversidade.
                random.shuffle(lista_aux)
                return lista_aux  # Retorna a população gerada.

    # Embaralha a ordem dos indivíduos para aumentar a diversidade.
    random.shuffle(lista_aux)

    # Retorna a população gerada.
    return lista_aux

def roleta(lista: list[float]) -> int:
    # Gera um valor aleatório entre 0 e a soma de todos os valores da lista.
    rand = random.random() * sum(lista)

    soma = 0
    for i, apt in enumerate(lista):
        # Incrementa a soma com a aptidão do indivíduo atual.
        soma += apt

        # Quando a soma acumulada atinge ou ultrapassa o valor randômico,
        # retorna o índice do indivíduo atual como o selecionado.
        if soma >= rand:
            return i


def calcular_dois_pontos(ponto1, ponto2):
    # Calcula a diferença entre as coordenadas x dos pontos e eleva ao quadrado.
    diff_x = (ponto1[0] - ponto2[0]) ** 2

    # Calcula a diferença entre as coordenadas y dos pontos e eleva ao quadrado.
    diff_y = (ponto1[1] - ponto2[1]) ** 2

    # Soma as diferenças das coordenadas x e y e tira a raiz quadrada para obter a distância Euclidiana.
    distPontos = (diff_x + diff_y) ** 0.5

    return distPontos


def calcular_todas_distancias(lista_cidades: List[List[list]]) -> List[float]:
    # Cria uma lista para armazenar as distâncias de cada rota.
    distancia_rotas = [None] * len(lista_cidades)

    # Itera por todas as rotas (listas de cidades) na lista de cidades.
    for i, rota in enumerate(lista_cidades):
        distancia = 0

        # Itera por todas as cidades na rota.
        for index, _ in enumerate(rota):
            if index < len(rota) - 1:
                # Calcula a distância entre a cidade atual e a próxima cidade na rota.
                distancia += calcular_dois_pontos(rota[index], rota[index + 1])

        # Adiciona a distância entre a última cidade e a primeira cidade para fechar o ciclo.
        distancia += calcular_dois_pontos(rota[-1], rota[0])

        # Armazena a distância total da rota na lista de distâncias das rotas.
        distancia_rotas[i] = distancia

    # Retorna a lista de distâncias das rotas.
    return distancia_rotas


def escala_apt(lista: List[float]) -> List[float]:
    valor_minimo = min(lista)
    valor_maximo = max(lista)
    lista_escalada = [(x - valor_minimo + 1) / (valor_maximo - valor_minimo + 1) for x in lista]
    return lista_escalada


def torneio(aptidao: List[float]) -> int:
    pai1 = random.randint(0, len(aptidao) - 1)
    pai2 = random.randint(0, len(aptidao) - 1)
    return pai1 if aptidao[pai1] > aptidao[pai2] else pai2


def mutacao_genes(lista_populacao: list[list[object]], taxa_mutacao: float):
    # Iterar sobre cada indivíduo na população
    for i, elemento in enumerate(lista_populacao):
        # Verificar se a mutação deve ocorrer com base na taxa de mutação
        if random.random() <= taxa_mutacao:
            # Gerar dois índices aleatórios diferentes dentro da faixa válida
            a, b = random.randint(0, len(elemento) - 1), random.randint(0, len(elemento) - 1)

            # Garantir que 'a' e 'b' sejam índices diferentes
            while a == b:
                b = random.randint(0, len(elemento) - 1)

            # Trocar os elementos nas posições 'a' e 'b' dentro do indivíduo
            lista_populacao[i][a], lista_populacao[i][b] = lista_populacao[i][b], lista_populacao[i][a]

    return lista_populacao


def aptidao(lista_populacao: List[float]) -> List[float]:
    # Inicializa uma lista para armazenar os valores de aptidão
    lista_aptidao = [None] * len(lista_populacao)

    # Itera sobre os elementos da lista_populacao
    for index, el in enumerate(lista_populacao):
        # Calcula a aptidão para cada elemento da população
        # Neste exemplo, calculamos o cosseno do valor multiplicado por 90 graus
        lista_aptidao[index] = cos(el * radians(90))

    return lista_aptidao


def selecao_pais(lista_populacao: List[list[list]], aptidao: List[float], sel_func: Callable) -> List[List[list]]:
    # Inicializa uma lista para armazenar os pais selecionados
    lista_pais: List[List[list]] = [None] * len(lista_populacao)

    # Itera sobre a população em pares (dois pais por vez)
    for i in range(0, len(lista_populacao), 2):
        # Seleciona o índice do primeiro pai usando a função de seleção (sel_func)
        idx_pai1_selecionado = sel_func(aptidao)

        # Cria uma lista de aptidão excluindo o primeiro pai selecionado
        aptidao_sem_pai1 = aptidao[:idx_pai1_selecionado] + aptidao[idx_pai1_selecionado + 1:]

        # Seleciona o índice do segundo pai usando a função de seleção (sel_func) na nova lista de aptidão
        idx_pai2_selecionado = sel_func(aptidao_sem_pai1)

        # Atribui os pais selecionados à lista de pais
        lista_pais[i] = lista_populacao[idx_pai1_selecionado]
        lista_pais[i + 1] = lista_populacao[idx_pai2_selecionado]

    return lista_pais


def PMX(father1, father2):
    # Escolhe dois pontos de corte aleatórios
    cutpoint1 = random.randint(0, len(father1) - 1)
    cutpoint2 = random.randint(0, len(father1) - 1)

    # Garante que cutpoint1 é menor que cutpoint2
    if cutpoint1 > cutpoint2:
        cutpoint1, cutpoint2 = cutpoint2, cutpoint1

    # Inicializa uma lista de filhos com os genes do primeiro pai
    sons = father1[:]

    # Mapeamento de genes do segundo pai para o primeiro pai dentro dos pontos de corte
    for i in range(cutpoint1, cutpoint2):
        # Se o gene do segundo pai não estiver na seção mapeada do primeiro pai
        if father2[i] not in sons[cutpoint1:cutpoint2]:
            # Encontra o índice correspondente do gene do segundo pai no primeiro pai
            j = father1.index(father2[i])

            # Realiza a troca dos genes entre os pais
            sons[i], sons[j] = sons[j], sons[i]

    # Repete o processo para garantir que todas as correspondências sejam tratadas
    for i in range(cutpoint1, cutpoint2):
        if father2[i] not in sons[cutpoint1:cutpoint2]:
            j = father1.index(father2[i])
            sons[j], sons[i] = sons[i], sons[j]

    return sons


def cruzamento_dois_pais(pai1, pai2, taxa_cruzamento) -> tuple:
    # Verifica se o cruzamento deve ocorrer com base na taxa de cruzamento
    if random.random() < taxa_cruzamento:
        # Realiza o cruzamento PMX entre os pais para gerar dois filhos
        return PMX(pai1, pai2), PMX(pai2, pai1)

    # Se a taxa de cruzamento não for atingida, os pais não sofrem cruzamento
    return pai1, pai2


def cruzamento_todos_pais(lista_pais: List, taxa_cruzamento: float) -> List:
    lista_filho = [None] * len(lista_pais)
    for i in range(0, len(lista_pais), 2):
        lista_filho[i], lista_filho[i + 1] = cruzamento_dois_pais(lista_pais[i], lista_pais[i + 1], taxa_cruzamento)
    return lista_filho


def evolucao(lista_populacao: List, numero_individuo: int, numero_geracoes: int,
             taxa_cruzamento: float, taxa_mutacao: float, sel_func: Callable) -> tuple[List[List[list]], List[float]]:
    # Inicializa a população com base na lista de cidades
    populacao_inicial = gerar_populacao_inicial(lista_populacao, numero_individuo)

    # Inicializa a variável para acompanhar o menor caminho encontrado
    menor_caminho = float('inf')

    # ‘Loop’ de evolução ao longo de um número fixo de gerações
    for geracao in range(numero_geracoes):
        # Calcula as distâncias de todas as rotas na população atual
        distancia = calcular_todas_distancias(populacao_inicial)

        # Encontra o melhor indivíduo (menor distância) na geração atual
        melhor_individuo = min(distancia)

        # Exibe informações sobre a geração atual
        # print(f'Geração: {geracao}ª Menor distância:', melhor_individuo)

        # Seleciona os pais com base na aptidão da população atual
        parentes = selecao_pais(populacao_inicial, aptidao(escala_apt(distancia)), sel_func)

        # Realiza o cruzamento entre os pais para criar os filhos
        sons = cruzamento_todos_pais(parentes, taxa_cruzamento)

        # Aplica mutação nos filhos gerados
        filhos_mutados = mutacao_genes(sons, taxa_mutacao)

        # Atualiza a população com os filhos mutados
        populacao_inicial = filhos_mutados[:]

        # Atualiza o menor caminho encontrado, se necessário
        if melhor_individuo < menor_caminho:
            menor_caminho = melhor_individuo

    # Exibe o menor caminho de todas as gerações
    print(f"Menor caminho de todas as gerações: {menor_caminho}")

    # Retorna a população final e a lista de distâncias
    return populacao_inicial, distancia


lista = []
a = 'berlin52.tsp'
with open(a) as obj_file:
    text = obj_file.readlines()

for i, el in enumerate(text[6:-1]):
    line = []
    for index, x in enumerate(el.replace('\n', ' ').split(' ')):
        if (x != ''):
            line.append(float(x))
    lista.append((line[1], line[2], str(int(line[0]))))


random.seed(0.4227137781497774)
ini = time.time()
evolucao(
    lista_populacao=lista,
    numero_individuo=80,
    numero_geracoes=8438,
    taxa_cruzamento=0.8108250947136191,
    taxa_mutacao=0.07512625785937284,
    sel_func=torneio
)
fim = time.time()
print("Tempo gasto:", round(fim - ini, 3))
