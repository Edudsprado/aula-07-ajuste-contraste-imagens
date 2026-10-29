# Aula 07 — Ajuste de contraste de imagens

Projeto acadêmico de **Computação Gráfica e Processamento de Imagens** para carregar uma imagem do mar, ajustar seu contraste com NumPy e comparar o resultado com a imagem original usando Matplotlib.

O código está comentado em português e organizado em seis partes. O principal parâmetro a modificar é `CONTRASTE`, definido no início de `00_base_carga_visualizacao.py`.

## Objetivo

Compreender como uma transformação linear aplicada às intensidades RGB altera a aparência de uma imagem. A atividade permite observar a separação entre regiões claras e escuras, a preservação das dimensões e a perda de detalhes quando intensidades ultrapassam os limites da escala.

## Imagem utilizada

![Imagem original do mar utilizada na atividade](mar.png)

- Arquivo: `mar.png`, PNG RGB com **639 × 360 pixels**.
- A imagem foi recuperada da pasta local da Aula 07 junto com o código comentado; foi copiada sem alteração dos bytes.
- SHA-256: `c3a736c0687bc9a4030f55e1a46559db857b97c307598f143bba2208fc9cba91`.
- Não foi criada nem baixada uma imagem para substituir o arquivo original.

O arquivo é incluído como material da atividade. A pasta de origem não informa autoria ou licença da imagem; este repositório não atribui uma licença de terceiros ao arquivo.

## Requisitos

- Python **3.12**, versão usada na verificação deste projeto.
- NumPy, para representar a imagem como uma matriz e executar as operações numéricas.
- Matplotlib, para ler a imagem, exibir a comparação e salvar a figura.
- Um ambiente gráfico para abrir a janela interativa. Em servidores ou terminais sem interface, é possível gerar apenas o arquivo PNG.
- Git é necessário apenas para clonar o repositório. VS Code é opcional.

As versões verificadas estão em `requirements.txt`. As demais dependências são instaladas automaticamente pelo `pip`; `pathlib` faz parte da biblioteca padrão do Python.

## Estrutura

```text
aula-07-ajuste-contraste-imagens/
├── 00_base_carga_visualizacao.py  # Código comentado da atividade
├── mar.png                      # Imagem original
├── README.md                    # Explicações e orientações
├── requirements.txt             # Dependências verificadas
└── .gitignore                   # Arquivos locais e gerados que não serão versionados
```

Depois da execução, `resultado.png` aparece na mesma pasta do script. Ele contém a figura comparativa e não é versionado. O ambiente virtual `.venv/`, os caches e as configurações locais do editor também são ignorados.

## Preparação e execução

### 1. Obter o projeto

```powershell
git clone https://github.com/Edudsprado/aula-07-ajuste-contraste-imagens.git
cd aula-07-ajuste-contraste-imagens
```

Também é possível usar **Code → Download ZIP** no GitHub e extrair os arquivos antes de continuar.

### 2. Instalar as dependências no Windows

No terminal PowerShell, dentro da pasta do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Esses comandos usam diretamente o Python do ambiente virtual, sem exigir a ativação por `Activate.ps1`. Caso o comando `py` não esteja disponível, use o executável `python` correspondente ao Python 3.12.

### 3. Executar

```powershell
.\.venv\Scripts\python.exe .\00_base_carga_visualizacao.py
```

O programa carrega `mar.png`, aplica o fator definido em `CONTRASTE`, imprime informações no terminal, salva `resultado.png` e abre uma janela com as duas imagens. Feche a janela para concluir a execução no terminal.

No VS Code, abra a pasta do projeto e selecione o interpretador `.venv\Scripts\python.exe` em **Python: Select Interpreter**, caso utilize a extensão Python. O terminal integrado pode executar os mesmos comandos acima.

### Linux e macOS

Com Python 3.12 disponível:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python 00_base_carga_visualizacao.py
```

### Executar sem janela gráfica

No PowerShell:

```powershell
$env:MPLBACKEND = "Agg"
.\.venv\Scripts\python.exe .\00_base_carga_visualizacao.py
Remove-Item Env:MPLBACKEND
```

No Linux/macOS:

```bash
MPLBACKEND=Agg .venv/bin/python 00_base_carga_visualizacao.py
```

O backend `Agg` salva `resultado.png` sem abrir uma janela. O Matplotlib pode avisar que a figura não é interativa; isso é esperado nesse modo.

## Como modificar o contraste

Abra `00_base_carga_visualizacao.py` e localize a seção **2. CONFIGURAÇÃO DO CONTRASTE**:

```python
CONTRASTE = 1.5
```

Troque o número, salve o arquivo e execute novamente. Use ponto como separador decimal no código Python.

| Fator | Efeito esperado | Uso na atividade |
| --- | --- | --- |
| `0.0` | Todos os canais ficam em 128, formando cinza uniforme | Entender o caso limite |
| `0.5` | Reduz bastante o contraste | Observar a aproximação das intensidades ao cinza |
| `0.8` | Reduz moderadamente o contraste | Comparar detalhes com menor separação tonal |
| `1.0` | Preserva os pixels da imagem carregada | Referência sem ajuste |
| `1.2` | Aumenta levemente o contraste | Avaliar um ajuste mais discreto |
| `1.5` | Aumenta o contraste; é o valor inicial | Destacar diferenças entre regiões claras e escuras |
| `1.8` ou `2.0` | Aumento mais forte, com maior possibilidade de saturação | Investigar perda de detalhes |

Os efeitos visuais dependem da distribuição de intensidades da imagem. Valores negativos invertem a relação das intensidades com o ponto de referência e não fazem parte do ajuste convencional proposto. O script não valida o fator; use números finitos e não negativos nestes experimentos.

Para trocar a imagem em uma atividade futura, altere `ARQUIVO = PASTA / "mar.png"`. A resolução do caminho parte da pasta do próprio script, e não da pasta em que o terminal foi aberto.

## Fórmula utilizada

Para cada intensidade de cada canal RGB:

```text
novo_pixel = (pixel - 128) * fator + 128
```

No código:

```python
img = imagem.astype(np.float32)
img = (img - 128) * fator + 128
img = np.clip(img, 0, 255)
return img.astype(np.uint8)
```

1. A conversão para `float32` permite subtrações e multiplicações sem o comportamento de estouro de uma operação direta em `uint8`.
2. Subtrair 128 desloca a referência para zero.
3. Multiplicar pelo fator afasta ou aproxima as intensidades dessa referência.
4. Somar 128 retorna à escala original.
5. `np.clip` limita as intensidades a `[0, 255]`.
6. A conversão para `uint8` produz novamente canais de 8 bits; as partes fracionárias dos valores já limitados são truncadas.

O valor **128 é a referência convencional adotada nesta atividade**. O ponto médio matemático de 0 a 255 é 127,5; 128 também não representa necessariamente a média da imagem nem um cinza perceptualmente central.

Exemplo com fator `1.5`:

| Intensidade original | Cálculo | Intensidade final |
| --- | --- | --- |
| 40 | `(40 - 128) * 1.5 + 128 = -4` | 0, após limitação |
| 80 | `(80 - 128) * 1.5 + 128 = 56` | 56 |
| 128 | `(128 - 128) * 1.5 + 128 = 128` | 128 |
| 180 | `(180 - 128) * 1.5 + 128 = 206` | 206 |
| 240 | `(240 - 128) * 1.5 + 128 = 296` | 255, após limitação |

## Explicação de cada parte do código

| Seção | Responsabilidade |
| --- | --- |
| 1. Configuração da imagem | Define `PASTA` e o caminho de `mar.png` com `pathlib` |
| 2. Configuração do contraste | Define o fator editável `CONTRASTE` |
| 3. `carregar_imagem` | Lê o arquivo, replica tons de cinza em três canais, descarta alpha e normaliza para RGB `uint8` |
| 4. `ajustar_contraste` | Aplica a fórmula a todos os canais com NumPy e limita o resultado |
| 5. `comparar` | Imprime dimensões e pixel central, cria dois painéis, salva a figura e tenta exibi-la |
| 6. Execução principal | Encadeia carregamento, ajuste e comparação quando o arquivo é executado diretamente |

O código comentado foi recuperado da versão local existente da Aula 07 e mantido sem alterações. Ele deriva da atividade de carregamento e visualização fornecida pelo professor, com a adaptação para a imagem do mar e o ajuste de contraste. Não foram acrescentados nomes de professor ou instituição que não estavam disponíveis.

### Comportamento quando a imagem não abre

A versão local já continha uma imagem sintética de teste, criada na memória com gradientes e formas geométricas, como alternativa em caso de falha de leitura. Esse comportamento foi preservado no código e é anunciado no terminal. Ele **não substitui o arquivo real `mar.png` versionado**.

Se aparecer a mensagem `Não foi possível abrir a imagem`, confira o nome, o caminho e a integridade do arquivo. Um resultado produzido a partir da alternativa sintética não deve ser interpretado como uma análise da imagem do mar. A alternativa tem 192 × 128 pixels; a imagem fornecida tem 639 × 360 pixels.

## Comparação lado a lado e interpretação

- **Esquerda — Original:** imagem carregada e convertida para RGB de 8 bits.
- **Direita — Contraste ajustado:** mesma imagem, com o fator indicado no título.
- **Terminal:** dimensões no formato `(altura, largura, canais)` e valores RGB do pixel central da imagem alterada.
- **`resultado.png`:** figura completa com os dois painéis e títulos, salva antes da abertura da janela em uma resolução de 130 dpi. Suas dimensões são as da figura, não as da imagem original.

Para a imagem incluída, a matriz possui dimensão `(360, 639, 3)`. O pixel central é acessado em `[180, 319]`; essa posição é calculada automaticamente para outras dimensões.

Com fator maior que 1, canais abaixo de 128 diminuem e canais acima de 128 aumentam. Avalie a separação entre os tons do mar, as regiões de sombra e as áreas claras. Um aumento pode destacar diferenças, mas também eliminar gradações. O fato de uma imagem parecer mais intensa não significa que contenha mais informação.

Com fator entre 0 e 1, os canais se aproximam de 128 e a imagem tende a parecer mais acinzentada. Com fator 1, os pixels carregados são preservados. O pixel central é apenas uma amostra: ele não descreve sozinho o contraste da imagem inteira.

**Roteiro de observação:** execute com `0.5`, `1.0`, `1.5` e `2.0`; registre as diferenças percebidas nas mesmas regiões. Cada execução sobrescreve `resultado.png`. Para conservar as comparações, copie ou renomeie o resultado entre as execuções, por exemplo para `comparacao_fator_1_5.png`.

## Limitações

- O ajuste é global: o mesmo fator é aplicado a todos os pixels, sem adaptação por região.
- Os canais RGB são tratados individualmente. Isso pode alterar a aparência das cores e a saturação; não há processamento exclusivo de luminância.
- A operação ocorre nos valores RGB codificados da imagem; não há linearização de luz nem gerenciamento de perfis de cor.
- A limitação em 0 e 255 perde informação de forma irreversível no resultado. Diminuir o contraste depois não recupera os detalhes cortados.
- O pivô 128 é fixo e não acompanha a média ou o histograma da imagem.
- O carregamento replica imagens em tons de cinza e descarta transparência sem composição com um fundo. O fluxo foi verificado com a imagem PNG RGB de 8 bits fornecida; imagens HDR, de 16 bits ou com formatos de canais incomuns exigem adaptação.
- A quantização para `uint8` pode introduzir pequenas diferenças por truncamento. O parâmetro não possui validação de tipo ou faixa.
- `vmin` e `vmax` não reescalam automaticamente uma imagem RGB `uint8`; a escala válida é garantida pelo processamento com `np.clip`.
- O resultado salvo é uma figura de comparação. O script não exporta a matriz alterada como uma imagem separada nem calcula métricas globais ou histogramas.
- A imagem de teste automática pode mascarar um erro no caminho se as mensagens do terminal não forem observadas.
- A avaliação visual depende do monitor e das condições de observação. Não há um fator universalmente melhor para todas as imagens.

## Possíveis próximos ajustes

1. Adicionar parâmetros de terminal para fator, imagem e destino, com validação de valores finitos e não negativos.
2. Tornar a imagem sintética uma opção explícita de demonstração e interromper a execução quando a imagem exigida não estiver disponível.
3. Salvar a imagem alterada separadamente, mantendo também o painel comparativo.
4. Exibir histogramas antes e depois e medir a proporção de canais que atingem 0 ou 255.
5. Comparar vários fatores na mesma figura ou adicionar um controle deslizante.
6. Investigar brilho, correção gama, normalização e equalização de histograma como transformações distintas.
7. Explorar um espaço de cor que permita modificar a luminância separadamente e avaliar a preservação das cores.
8. Estudar um pivô adaptável e métodos de contraste local, documentando a diferença em relação à fórmula desta aula.

Esses itens são sugestões para evoluir a atividade; não estão implementados nesta versão.

## Verificação

A versão publicada foi executada com Python 3.12.3, NumPy 2.5.4 e Matplotlib 3.11.2, usando a imagem incluída e o backend `Agg`. Foram conferidos o carregamento RGB, a preservação da imagem de entrada, o fator 1, o caso fator 0, a limitação das intensidades e a geração da figura comparativa com fator 1.5. O arquivo `mar.png` foi conferido por SHA-256 contra a cópia local de origem.

## Créditos e uso acadêmico

Projeto organizado na conta **Edudsprado** para a Aula 07 de Computação Gráfica e Processamento de Imagens. Código baseado no exercício do professor e na adaptação local comentada. Não foi adicionada uma licença de redistribuição para material cuja titularidade não está identificada na pasta da atividade.
