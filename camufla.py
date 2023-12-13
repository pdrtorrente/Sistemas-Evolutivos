import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Função para gerar a população inicial aleatória de 900 indivíduos com valores RGB
def gerar_populacao_inicial(tamanho_populacao):
    return np.random.randint(0, 256, size=(tamanho_populacao, 3))

# Função para calcular o fitness de cada indivíduo
def calcular_fitness(populacao, cor=[255, 0, 0]):
    return np.linalg.norm(populacao - cor, axis=1)

# Função para ordenar os indivíduos do mais adaptado para o menos
def ordena(array, i = 0):
    return sorted(array, key=lambda x: x[i])

# Função para seleção dos indivíduos mais adaptados, considerando a taxa de genocídio
def selecao(pop_fitness, tamanho_populacao, taxa_genocidio):
    quantidade_selecionada = int(tamanho_populacao * (1 - taxa_genocidio))
    return np.argsort(pop_fitness)[:quantidade_selecionada]

# Função para cruzamento (crossover)
def crossover(pais, tamanho_populacao):
    filhos = np.empty((tamanho_populacao - len(pais), 3), dtype=int)
    for i in range(0, len(filhos)):
        pai_idx = np.random.randint(0, len(pais))
        mae_idx = np.random.randint(0, len(pais))
        filhos[i] = (pais[pai_idx] + pais[mae_idx]) / 2
    return filhos

# Função para mutação
def mutacao(filhos, taxa_mutacao=0.01):
    for i in range(len(filhos)):
        if np.random.random() < taxa_mutacao:
            filhos[i] = np.random.randint(0, 256, size=3)
    return filhos

# Função para plotar a população com o número da população
def plotar_populacao(populacao, iteracao, ims, fig, ax):
    ax.clear()
    imagem = populacao.reshape(30, 30, 3)
    ax.imshow(imagem)
    ax.text(0.5, 1.05, f'População: {iteracao}', horizontalalignment='center', transform=ax.transAxes, fontsize=12)
    ims.append([ax])

# Função para substituir os indivíduos menos camuflados com os filhos dos que mais mais camuflados
def genocidio(taxa_genocidio, populacao, array_fit_ind, filhos): 
    # Atualização da população com os filhos gerados, substituindo os menos aptos
    for j in range(900 - len(filhos), 900):
        populacao[array_fit_ind[j][1]] = filhos[j - (900 - len(filhos))]

# Simulação do algoritmo genético
def simulacao_algoritmo_genetico(iteracoes, cor_camuflagem, taxa_genocidio=0.5):    # Geração da população inicial
    populacao = gerar_populacao_inicial(900)

    fig, ax = plt.subplots()
    ax.axis('off')

    ims = []
    plotar_populacao(populacao, 0, ims, fig, ax)

    def update(frame):
        nonlocal populacao
        # Cálculo do fitness
        fitness = calcular_fitness(populacao, cor_camuflagem)

        # Criando array que armazena índice do indivíduo e seu "fitness"
        array_fit_ind = [(fit, ind) for ind, fit in enumerate(fitness)]

        # Ordenando o array com os índices 
        array_fit_ind = ordena(array_fit_ind, 0)

        # Seleção dos indivíduos mais adaptados
        indices_selecionados = selecao(fitness, len(populacao), taxa_genocidio)
        populacao_selecionada = populacao[indices_selecionados]

        # Cruzamento (crossover)
        filhos = crossover(populacao_selecionada, 900)

        # Mutação
        filhos_mutados = mutacao(filhos)

        # Genocídio
        genocidio(taxa_genocidio, populacao,array_fit_ind, filhos_mutados)

        # Mantém pelo menos um indivíduo para evitar a extinção total da população
        if len(indices_selecionados) == 0:
            populacao[fitness.argmin()] = filhos_mutados[0]

        plotar_populacao(populacao, frame + 1, ims, fig, ax)

    ani = FuncAnimation(fig, update, frames=iteracoes, interval=50, blit=False, repeat=False)
    plt.show()

# Rodar a simulação com 100 iterações e taxa de genocídio de 40%
simulacao_algoritmo_genetico(1000, cor_camuflagem=[255, 0, 0], taxa_genocidio=0.1)