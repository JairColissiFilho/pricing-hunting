# Pricing Hunting

Buscador de preços que consulta produtos na Kabum e mostra resultados com imagem, preço e link direto, com filtro por categoria e ordenação por preço.

Projeto de estudo em Python (web scraping, Flask e pandas) e JavaScript puro no front-end.

## Funcionalidades

- Busca produtos em tempo real na Kabum
- Mostra imagem, nome, preço (com e sem desconto) e link do produto
- Classifica cada produto por categoria (placa de vídeo, PC gamer, notebook, etc.)
- Filtro por categoria e ordenação por menor/maior preço
- Histórico de preços: salva as buscas em CSV, um snapshot por dia, para acompanhar variação de preço ao longo do tempo

## Tecnologias

- **Python**: `requests` + `BeautifulSoup` para o scraping, `Flask` como servidor web, `pandas` para o histórico em CSV
- **JavaScript, HTML e CSS**: front-end simples, sem framework

## Estrutura do projeto

```
kabum.py           # scraper: busca produtos na Kabum e extrai nome, preço, imagem e link
classificacao.py   # classifica cada produto por categoria, condição (novo/usado) e tags
app.py             # servidor Flask: serve a página e a API de busca
tabelas.py         # roda o scraper e salva o histórico de preços em tabelas/kabum.csv
static/
  index.html       # página
  css/style.css
  js/app.js        # busca, filtro e ordenação no navegador
```

## Como rodar

1. Instalar as dependências:

   ```
   pip install -r requirements.txt
   ```

2. Rodar o servidor:

   ```
   python app.py
   ```

3. Abrir no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Coletar histórico de preços

Para salvar a busca de hoje em `tabelas/kabum.csv` (acumulando um snapshot por dia):

```
python tabelas.py
```

O termo buscado é definido pela variável `BUSCA` no início do arquivo.

## Como funciona a classificação

A Kabum mistura no mesmo resultado tipos de produto diferentes — por exemplo, uma busca por "GTX 3060" retorna tanto placas de vídeo quanto PCs completos com essa placa. O `classificacao.py` resolve isso com regras de palavras-chave sobre o nome do produto, permitindo separar por categoria na interface. (Ainda em otimização)

## Próximos passos

- Adicionar outros sites de venda além da Kabum
- Comparar preço do mesmo produto entre sites
- Classificar a categoria a partir da categoria oficial do site (mais preciso que só palavra-chave)
