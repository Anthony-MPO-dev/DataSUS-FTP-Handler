# Projeto de Download de Dados do Datasus

Este projeto oferece duas formas de baixar dados do **Datasus**: **via FTP** e **via Web Scraping** utilizando **Selenium**. A escolha do método de download pode ser configurada diretamente no script.

## Instalação e Configuração do Projeto

Este projeto utiliza **Poetry** para gerenciamento de dependências e ambiente virtual. Não há necessidade de um arquivo `requirements.txt`, pois o Poetry gerencia todas as dependências do projeto.

### 1. **Instalar Poetry**

Se você ainda não possui o Poetry instalado, pode instalá-lo com o seguinte comando:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. **Clonar o repositório do projeto**

Clone o repositório do projeto para o seu diretório local:

```bash
git clone <URL_DO_REPOSITORIO>
cd <DIRETORIO_DO_PROJETO>
```

### 3. **Instalar as dependências**

Com o Poetry instalado, basta rodar o seguinte comando para instalar as dependências do projeto:

```bash
poetry install
```
Esse comando irá configurar o ambiente virtual e instalar todas as dependências necessárias.

### 4. **Instalar as dependências de desenvolvimento (se necessário, no nosso caso ainda não é)**
Caso precise de dependências extras (o que não deve ser o caso) para desenvolvimento, como para testes, pode rodar:

```bash
poetry install --dev
```

### 5. **Ativar o ambiente virtual do Poetry**
Para ativar o ambiente virtual onde as dependências do projeto estão instaladas, utilize o comando:

```bash
poetry shell
```


## Modos de Download de Dados
O projeto oferece duas formas de baixar os dados: modo FTP e modo Web Scraping. Escolha o método que melhor se adapta ao seu caso.

### 1. **Modo FTP (Download via FTP)**
O modo FTP utiliza um link direto para baixar os arquivos dos dados. Ao rodar o script ele automaticamente esta configurado para rodar no modo FTP, ele irá conectar ao servidor FTP do Datasus, acessar o diretório apropriado e fazer o download dos arquivos.

Como usar:
apenas abra os arquivos do projeto e navegue até a pasta src/

```bash
cd DataSUS-FTP-Handler/src/
```

Parametros para execução: **-t TU** <- inicializara o programa para baixar e tratar os arquivos de Tuberculose 

```bash
python3 search.py -t TU
```

2. Modo Web Scraping (Download via Selenium)
O modo Web Scraping utiliza o Selenium para automatizar a navegação no site do Datasus e baixar os arquivos diretamente pela interface web. Isso é útil caso o link direto não esteja disponível ou você precise navegar pelo site para localizar os arquivos, porem eu desabilitei esse modo, então boa sorte se quiser reativar hehe.

Como usar:
No script, ao selecionar o modo Web Scraping, o Selenium irá abrir um navegador (geralmente em modo headless, sem interface gráfica) e simular os cliques necessários para acessar e fazer o download dos arquivos.

OBS: o comando é o mesmo para ativação do programa: 
```bash
python3 search.py -t TU
```

# Como Rodar o Script
## Para rodar o script no modo FTP, utilize o seguinte comando:

### 1. **Você pode usar o seguinte argumentos indicando --tema ou -t para o tema da pesquisa e --clean para limpar arquivos obsoletos ou resto de arquivos não mais necessarios depois da execução:**
```bash
python3 search.py -t TU --clean
```
### 1. **Você pode usar os argumentos -y ou --years para definir um periodo especifico para o search exemplo:**

Year range in 'YYYY-YYYY' format. Example: --years 2001-2005.

```bash
python3 search.py -t TU -years 2001-2005 -c

# OBS: -c é o parametro --clean opcional
```

## Dependências
As dependências principais do projeto são gerenciadas pelo Poetry e estão especificadas no arquivo pyproject.toml. Abaixo estão as dependências utilizadas:

- Python: ^3.12
- pyreaddbc: 1.2.0
- pandas: *
- numpy: *
- pyarrow: ^17.0.0
- fastparquet: ^2024.5.0
- blue: *
- isort: *
- selenium: *
- requests: ^2.32.3
- unidecode: ^1.3.8
- bs4: ^0.0.2
- dbfread: ^2.0.7

Estas dependências cobrem a conexão via FTP, a automação com Selenium, manipulação de dados com pandas e numpy, e outras ferramentas úteis como unidecode e requests.

## Contribuição
Se você deseja contribuir com o projeto, fique à vontade para abrir issues ou pull requests. Toda contribuição é bem-vinda!