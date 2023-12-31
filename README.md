# Geração de imagem com algoritmo genético
O objetivo do projeto é fazer um programa com algoritmo genético que gere uma imagem do zero com base em uma imagem de exemplo.

Este projeto foi realizado na disciplina **SCC0713 - Sistemas Evolutivos Aplicados à Robótica** para fins educacionais.

Link da apresentação: https://drive.google.com/file/d/1w_VU63lqRdXGpKfya93BiFihopZSRkfZ/view?usp=drive_link

## Funcionamento do programa
O programa funciona da seguinte forma:
* É gerada uma população inicial em que cada indivíduo representa um pixel da imagem com seus valores no espectro RGB;
* Para cada indivíduo calcula-se seu "fitness" com base no pixel de referência da foto original;
* Os 50% melhores indivíduos serão selecionados para gerarem os "filhos", já a outra metade dos piores sofrerá  o "genocídio";
* Os filhos serão gerados por meio de um crossover (média dos valores) entre dois indivíduos "pais" selecionados anteriormente;
* Alguns indivíduos da população sofrerá uma mutação para evitar mínimos locais;
* Repete-se todo o processo nas outras gerações.

Foi escolhido o formato **.ppm** devido a sua facilidade para manipulação de pixels e por não haver compressão, não há perda de dados da imagem.

## Programa em execução

### Programa de camuflagem com base em uma cor definida:

![camuflagem](https://github.com/pdrtorrente/Sistemas-Evolutivos/assets/83795403/6eabd161-e171-444f-9554-ed3356a2dced)

### Geração de imagem:

![programa-rodando](https://github.com/pdrtorrente/Sistemas-Evolutivos/assets/83795403/7ecbcb57-cac9-4042-bbb1-88c239d7736c)

### Média do fitness da população ao longo das gerações (quanto mais próximo de zero, melhores o indivíduos)

![media-fitness](https://github.com/pdrtorrente/Sistemas-Evolutivos/assets/83795403/d6a46c98-89af-4d0c-93ae-aacb1502f017)

## Getting Started

### Requerimentos
* Numpy
* Matplotlib
* Python

**Para executar o programa**

Primeiramente clone o repositório;

Execute o programa com o seguinte comando:
```
python3 gera_imagem.py
```
Ou para a camuflagem em cor:
```
python3 camuflagem.py
```
## Observações
Para colocar outras imagens de exemplo, adicione no mesmo repositório uma imagem no formato **.ppm** com o nome "exemplo.ppm".

## Autores
- Agnes Bressan de Almeida - 13677100
- Beatriz Lomes da Silva - 12548038
- Carolina Elias de Almeida Américo - 13676687
- Caroline Severiano Clapis - 13861923
- Pedro Oliveira Torrente - 11798853
