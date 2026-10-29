
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# 1. CONFIGURAÇÃO DA IMAGEM
# ==========================================================

# Identifica automaticamente a pasta onde está este código.
PASTA = Path(__file__).resolve().parent

# Seleciona a imagem que será analisada.
# Para utilizar outra imagem, altere apenas o nome abaixo.
ARQUIVO = PASTA / "mar.png"


# ==========================================================
# 2. CONFIGURAÇÃO DO CONTRASTE
# ==========================================================

# ALTERE ESTE VALOR PARA TESTAR O CONTRASTE DA IMAGEM.
#
# CONTRASTE = 1.0 -> imagem original (sem alteração)
# CONTRASTE = 0.5 -> contraste reduzido
# CONTRASTE = 0.8 -> contraste levemente reduzido
# CONTRASTE = 1.5 -> contraste aumentado
# CONTRASTE = 2.0 -> contraste muito aumentado
#
# Você pode testar outros valores, como 1.2 ou 1.8.

CONTRASTE = 1.5


# ==========================================================
# 3. FUNÇÃO PARA CARREGAR A IMAGEM
# ==========================================================

def carregar_imagem(arquivo=None):

    # Verifica se foi informado o caminho de uma imagem.
    if arquivo:
        try:

            # Lê a imagem usando Matplotlib.
            img = plt.imread(arquivo)

            # Se a imagem estiver em tons de cinza,
            # transforma em três canais RGB.
            if img.ndim == 2:
                img = np.stack([img] * 3, axis=-1)

            # Mantém apenas os três primeiros canais (RGB).
            # Remove o canal alpha, caso exista.
            img = img[:, :, :3]

            # Algumas imagens possuem valores entre 0 e 1.
            # Multiplicamos por 255 para trabalhar na escala
            # tradicional de intensidade de pixels.
            if np.issubdtype(img.dtype, np.floating):
                img = img * 255

            # Garante valores entre 0 e 255.
            return np.clip(img, 0, 255).astype(np.uint8)

        except (FileNotFoundError, OSError, ValueError) as e:
            print("Não foi possível abrir a imagem:", e)
            print("Usando a imagem de teste produzida na memória.")

    # ------------------------------------------------------
    # IMAGEM DE TESTE (CASO O ARQUIVO NÃO SEJA ENCONTRADO)
    # ------------------------------------------------------

    y, x = np.mgrid[0:128, 0:192]

    # Cria uma imagem RGB vazia.
    img = np.zeros((128, 192, 3), dtype=np.uint8)

    # Define gradientes de cores.
    img[:, :, 0] = np.clip(x * 255 / 191, 0, 255).astype(np.uint8)
    img[:, :, 1] = np.clip(y * 255 / 127, 0, 255).astype(np.uint8)
    img[:, :, 2] = 70

    # Adiciona um retângulo amarelo.
    img[35:95, 65:125] = [255, 210, 30]

    # Cria um círculo azul.
    mask = (x - 145) ** 2 + (y - 38) ** 2 <= 23 ** 2
    img[mask] = [20, 90, 240]

    return img


# ==========================================================
# 4. FUNÇÃO PARA AJUSTAR O CONTRASTE
# ==========================================================

def ajustar_contraste(imagem, fator):

    # Converte a imagem para float.
    # Isso permite fazer operações matemáticas sem
    # problemas de estouro dos valores uint8.
    img = imagem.astype(np.float32)

    # Aplica a fórmula de ajuste linear de contraste:
    #
    # NOVO_PIXEL = (PIXEL - 128) * FATOR + 128
    #
    # PIXEL: intensidade original
    # 128: ponto médio da escala de 0 a 255
    # FATOR: intensidade do contraste escolhida
    #
    # Fator > 1: aumenta o contraste
    # Fator = 1: mantém o contraste
    # 0 <= Fator < 1: reduz o contraste

    img = (img - 128) * fator + 128

    # Limita os valores ao intervalo permitido.
    #
    # Valores abaixo de 0 tornam-se 0 (preto).
    # Valores acima de 255 tornam-se 255 (branco).
    img = np.clip(img, 0, 255)

    # Retorna ao formato de imagem RGB uint8.
    return img.astype(np.uint8)


# ==========================================================
# 5. FUNÇÃO PARA COMPARAR AS IMAGENS
# ==========================================================

def comparar(original, alterada, titulo):

    # Identifica a altura e a largura da imagem.
    altura, largura = alterada.shape[:2]

    # Mostra no terminal as dimensões e o valor RGB
    # do pixel localizado no centro da imagem alterada.
    print(
        titulo,
        "| dimensão:", original.shape,
        "| pixel central:",
        alterada[altura // 2, largura // 2]
    )

    # Cria dois espaços para exibir as imagens lado a lado.
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    # Exibe a imagem original à esquerda
    # e a imagem com contraste alterado à direita.
    for ax, im, nome in zip(
        axes,
        [original, alterada],
        ["Original", titulo]
    ):
        ax.imshow(im, vmin=0, vmax=255)
        ax.set_title(nome)
        ax.axis("off")

    # Ajusta o espaçamento entre as imagens.
    plt.tight_layout()

    # Salva o resultado na pasta do projeto.
    resultado = PASTA / "resultado.png"

    fig.savefig(resultado, dpi=130)

    print("Resultado salvo em:", resultado)

    # Abre a janela com a comparação.
    try:
        plt.show()
    except Exception as e:
        print("Painel gráfico indisponível:", e)

    plt.close(fig)


# ==========================================================
# 6. EXECUÇÃO PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    # Carrega a imagem original do mar.
    original = carregar_imagem(ARQUIVO)

    # Aplica o fator de contraste definido na seção 2.
    alterada = ajustar_contraste(original, CONTRASTE)

    # Mostra a comparação entre as duas imagens.
    comparar(
        original,
        alterada,
        f"Contraste ajustado: {CONTRASTE}"
    )
