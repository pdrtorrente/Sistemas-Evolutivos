import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from PIL import Image

def ler_imagem_ppm(caminho):
    with open(caminho, 'rb') as arquivo:
        # Lê cabeçalho PPM
        magic_number = arquivo.readline().decode().strip()
        if magic_number != 'P6':
            raise ValueError("O arquivo não é um arquivo PPM binário (magic number P6 ausente)")

        # Ignora linhas de comentário
        while True:
            linha = arquivo.readline().decode().strip()
            if not linha.startswith('#'):
                break

        # Lê dimensões
        largura, altura = map(int, linha.split())

        # Lê valor máximo
        valor_maximo = int(arquivo.readline().decode().strip())

        # Lê os dados da imagem
        dados_imagem = arquivo.read()

    return largura, altura, valor_maximo, dados_imagem

def salvar_imagem_ppm(caminho, largura, altura, valor_maximo, dados_imagem):
    with open(caminho, 'wb') as arquivo:
        # Escreve cabeçalho PPM
        arquivo.write(b'P6\n')
        arquivo.write(f'{largura} {altura}\n'.encode())
        arquivo.write(f'{valor_maximo}\n'.encode())

        # Escreve os dados da imagem
        arquivo.write(dados_imagem)

# Exemplo de uso
caminho_entrada = 'exemplo.ppm'

# Ler imagem PPM
largura, altura, valor_maximo, dados_imagem = ler_imagem_ppm(caminho_entrada)
pixels = bytearray(dados_imagem)

TAMANHO_POPULACAO = largura*altura


# Função para gerar a população inicial aleatória com TAMANHO_POPULACAO indivíduos com valores RGB
def gerar_populacao_inicial(tamanho_populacao):
    return np.random.randint(0, 256, size=(tamanho_populacao, 3))

# Função para calcular o fitness de cada indivíduo
def calcular_fitness(populacao, pixels):
    # Verifica se o tamanho de pixels é compatível com o tamanho da população
    assert len(pixels) == len(populacao) * 3, "Tamanho incompatível de pixels"

    # Redimensiona o array de pixels para ser compatível com a população
    pixels = np.array(pixels).reshape(-1, 3)

    # Calcula a diferença absoluta para cada canal de cor
    diferenca_absoluta = np.abs(populacao - pixels)

    # Calcula o fitness como a norma Euclidiana para cada indivíduo
    fitness = np.linalg.norm(diferenca_absoluta, axis=1)

    return fitness

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
    imagem = populacao.reshape(altura, largura, 3)
    ax.imshow(imagem)
    ax.text(0.5, 1.05, f'População: {iteracao}', horizontalalignment='center', transform=ax.transAxes, fontsize=12)
    ims.append([ax])

# Função para substituir os indivíduos menos camuflados com os filhos dos que mais mais camuflados
def genocidio(taxa_genocidio, populacao, array_fit_ind, filhos): 
    # Atualização da população com os filhos gerados, substituindo os menos aptos
    for j in range(TAMANHO_POPULACAO - len(filhos), TAMANHO_POPULACAO):
        populacao[array_fit_ind[j][1]] = filhos[j - (TAMANHO_POPULACAO - len(filhos))]

# Simulação do algoritmo genético
def simulacao_algoritmo_genetico(iteracoes, pixels, taxa_genocidio = 0.1, intervalo = 100):    # Geração da população inicial
    populacao = gerar_populacao_inicial(TAMANHO_POPULACAO)

    fig, ax = plt.subplots()
    ax.axis('off')

    ims = []
    plotar_populacao(populacao, 0, ims, fig, ax)

    def update(frame):
        nonlocal populacao
        # Cálculo do fitness
        fitness = calcular_fitness(populacao, pixels)
        print(np.average(fitness))

        # Criando array que armazena índice do indivíduo e seu "fitness"
        array_fit_ind = [(fit, ind) for ind, fit in enumerate(fitness)]

        # Ordenando o array com os índices 
        array_fit_ind = ordena(array_fit_ind, 0)

        # Seleção dos indivíduos mais adaptados
        indices_selecionados = selecao(fitness, len(populacao), taxa_genocidio)
        populacao_selecionada = populacao[indices_selecionados]

        # Cruzamento (crossover)
        filhos = crossover(populacao_selecionada, TAMANHO_POPULACAO)

        # Mutação
        filhos_mutados = mutacao(filhos)

        # Genocídio
        genocidio(taxa_genocidio, populacao,array_fit_ind, filhos_mutados)

        # Mantém pelo menos um indivíduo para evitar a extinção total da população
        if len(indices_selecionados) == 0:
            populacao[fitness.argmin()] = filhos_mutados[0]

        plotar_populacao(populacao, frame + 1, ims, fig, ax)

    ani = FuncAnimation(fig, update, frames=iteracoes, interval=intervalo, blit=False, repeat=False)
    plt.show()

assert len(pixels) == TAMANHO_POPULACAO * 3, "Tamanho incompatível de pixels"

# Rodar a simulação com 500 iterações e taxa de genocídio de 10%
simulacao_algoritmo_genetico(100, pixels, taxa_genocidio = 0.1, intervalo = 100)
