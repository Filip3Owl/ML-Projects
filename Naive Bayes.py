from statistics import mean  # 📊 Para calcular médias
from math import sqrt, pi, exp  # ➗📐 Constantes e funções matemáticas

# 🔄 Converte valores de texto (strings) da classe para inteiros
def str_para_int(dataset, coluna):
    classes = [linha[coluna] for linha in dataset]  # 🧾 Coleta os valores da coluna de classe
    classes_unicas = set(classes)  # 🧬 Encontra os valores únicos (ex: 'maçã', 'laranja')
    mapa_classes = {valor: i for i, valor in enumerate(classes_unicas)}  # 🗺️ Mapeia cada classe para um número
    for linha in dataset:
        linha[coluna] = mapa_classes[linha[coluna]]  # 🔢 Substitui o valor de texto por número
    return mapa_classes

# 📦 Agrupa os dados com base na classe (ex: todas as 'maçãs' juntas)
def separar_por_classe(conjunto_dados):
    dados_separados = dict()
    for linha in conjunto_dados:
        valor_classe = linha[-1]  # 🏷️ Última coluna é a classe
        if valor_classe not in dados_separados:
            dados_separados[valor_classe] = []  # 📂 Cria nova lista para a classe
        dados_separados[valor_classe].append(linha)  # ➕ Adiciona linha ao grupo correspondente
    return dados_separados

# 📐 Calcula o desvio padrão (quanto os valores variam em relação à média)
def desvio_padrao(numeros):
    media = mean(numeros)  # 📊 Calcula média
    variancia = sum([(x - media)**2 for x in numeros]) / float(len(numeros) - 1)  # ⚖️ Calcula variância
    return sqrt(variancia)  # 🧮 Raiz quadrada da variância = desvio padrão

# 🧾 Resume cada atributo com média, desvio padrão e quantidade de exemplos
def resumir_conjunto_dados(conjunto_dados):
    resumos = [(mean(coluna), desvio_padrao(coluna), len(coluna)) for coluna in zip(*conjunto_dados)]
    del(resumos[-1])  # 🚫 Remove o resumo da coluna da classe (não precisa resumir classe)
    return resumos

# 📋 Cria resumos para cada classe separadamente
def resumir_por_classe(conjunto_dados):
    dados_separados = separar_por_classe(conjunto_dados)  # 📦 Agrupa por classe
    resumos = dict()
    for valor_classe, linhas in dados_separados.items():
        resumos[valor_classe] = resumir_conjunto_dados(linhas)  # 📝 Cria resumo por classe
    return resumos

# 🔢 Fórmula da distribuição normal (curva em forma de sino)
def calcular_probabilidade(x, media, desvio):
    exponente = exp(-((x - media)**2 / (2 * desvio**2)))  # 🎯 Parte exponencial da fórmula
    return (1 / (sqrt(2 * pi) * desvio)) * exponente  # 🔍 Fórmula da distribuição normal

# 📈 Calcula probabilidade de uma amostra pertencer a cada classe
def calcular_probabilidades_classes(resumos, linha):
    total_linhas = sum([resumos[classe][0][2] for classe in resumos])  # 🧮 Total de amostras
    probabilidades = dict()
    for valor_classe, resumo_classe in resumos.items():
        probabilidades[valor_classe] = resumos[valor_classe][0][2] / float(total_linhas)  # 📊 Probabilidade inicial (frequência)
        for i in range(len(resumo_classe)):
            media, desvio, _ = resumo_classe[i]
            probabilidades[valor_classe] *= calcular_probabilidade(linha[i], media, desvio)  # ➗ Multiplica pela probabilidade do atributo
    return probabilidades

# 🔮 Determina qual classe tem maior probabilidade
def prever(resumos, linha):
    probabilidades = calcular_probabilidades_classes(resumos, linha)  # 📊 Pega todas as probabilidades
    melhor_classe, melhor_prob = None, -1
    for valor_classe, prob in probabilidades.items():
        if melhor_classe is None or prob > melhor_prob:  # 🔎 Compara para encontrar a maior
            melhor_prob = prob
            melhor_classe = valor_classe
    return melhor_classe  # 🏁 Classe com maior probabilidade

# 🧪 Execução com dados fictícios
if __name__ == "__main__":
    # 🍎🍊 Dados fictícios: [tamanho, peso, classe]
    dados_ficticios = [
        [7.0, 150.0, 'maçã'],
        [6.5, 130.0, 'maçã'],
        [7.2, 160.0, 'maçã'],
        [5.5, 120.0, 'laranja'],
        [5.0, 110.0, 'laranja'],
        [5.2, 115.0, 'laranja']
    ]

    # 🔢 Converte as classes 'maçã' e 'laranja' para números
    mapa_classes = str_para_int(dados_ficticios, 2)

    # 🧠 Treina o modelo com os dados
    modelo = resumir_por_classe(dados_ficticios)

    # 🧾 Nova fruta para classificar: [tamanho, peso]
    nova_amostra = [6.8, 140.0]

    # 🔍 Faz a previsão com base nos dados anteriores
    classe_prevista = prever(modelo, nova_amostra)

    # 🖨️ Mostra o nome da classe prevista
    classe_nome = list(mapa_classes.keys())[list(mapa_classes.values()).index(classe_prevista)]
    print(f"📌 Nova amostra: {nova_amostra} → 🧠 Classe prevista: {classe_nome}")
