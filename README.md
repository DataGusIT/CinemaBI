
# Projeto de BI para Cinema - Da Modelagem ao Dashboard

> Projeto acadêmico completo de Business Intelligence, abordando desde a modelagem de dados relacional e dimensional até a criação de uma pipeline de dados com Python e a visualização em um dashboard no Power BI.

[![Status](https://img.shields.io/badge/Status-Concluído-success)](https://github.com/seu-usuario/projeto-bi-cinema)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-Pipeline-3776AB)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## Sobre o Projeto

Este projeto foi desenvolvido como parte de uma avaliação acadêmica com o objetivo de aplicar na prática o ciclo completo de um projeto de Business Intelligence. A partir de um problema de negócio para uma rede de cinemas, foram executadas as seguintes etapas:

1.  **Análise de Requisitos:** Entendimento das necessidades de controle de cinemas, filmes e público.
2.  **Modelagem de Dados:** Criação de dois modelos de dados distintos:
    *   Um **modelo convencional (transacional)**, otimizado para operações do dia a dia (ERP).
    *   Um **modelo dimensional (Star Schema)**, otimizado para análises e consultas de BI.
3.  **Pipeline de Dados (ETL):** Desenvolvimento de scripts em Python para gerar e processar dados, populando o modelo de BI.
4.  **Visualização de Dados:** Construção de um dashboard interativo no Power BI para validar o modelo dimensional e extrair insights sobre o público e a performance dos cinemas.

## 🖼️ Demonstração Visual

| Dashboard Final | Modelagem de BI (Star Schema) | Modelagem Convencional (ERP) |
| :---: | :---: | :---: |
| <img width="1646" height="976" alt="Image" src="https://github.com/user-attachments/assets/e8b16ec0-fc53-4dcc-af07-feac68f00628" /> | ![Modelo Dimensional Star Schema](link-para-sua-imagem-do-modelo-bi) | ![Modelo Transacional ERP](link-para-sua-imagem-do-modelo-convencional) |

## ✨ Funcionalidades

### 1. Modelagem de Dados
-   **Modelo Convencional (ERP):** Estrutura normalizada para garantir a integridade dos dados em operações de inserção, atualização e exclusão (CRUD).
-   **Modelo Dimensional (BI):** Estrutura em **Star Schema** com uma tabela Fato central (`fato_publico`) e Dimensões (`dim_cinema`, `dim_filme`, `dim_tempo`, etc.), otimizada para performance em consultas analíticas.

### 2. Pipeline de Dados (ETL com Python)
-   **Geração de Dados Sintéticos Realistas (`gerar_dados_massivos.py`):**
    -   Cria um grande volume de dados de sessões e espectadores.
    -   Utiliza lógica com pesos para simular uma ocupação de cinema realista (ex: mais público nos fins de semana e para filmes blockbusters).
-   **Transformação e Carga (`gerar_tabelas_excel.py`):**
    -   Lê os dados brutos gerados.
    -   Transforma os dados para o formato do modelo Star Schema, criando as tabelas Fato, Dimensões e Bridges.
    -   Carrega os dados transformados em arquivos Excel, prontos para serem consumidos pelo Power BI.

### 3. Dashboard Interativo no Power BI
-   **Análise de Público:** KPIs sobre o total de espectadores, distribuição por gênero, faixa etária e gênero de filme preferido.
-   **Tendência Temporal:** Gráfico de linhas que mostra a tendência de público ao longo dos meses.
-   **Performance de Filmes:** Ranking dos filmes com maior audiência.
-   **Filtros Dinâmicos:** Permite filtrar toda a análise por cinema, facilitando a comparação de desempenho entre as unidades.

## Tecnologias

### BI e Visualização
-   **Power BI** - Ferramenta principal para criação do dashboard.
-   **DAX** - Para métricas e cálculos no Power BI.

### Pipeline de Dados (ETL)
-   **Python** - Linguagem principal para os scripts.
-   **Pandas** e **Numpy** - Bibliotecas para manipulação e geração de dados.

### Modelagem
-   **Star Schema** - Metodologia utilizada para o modelo de BI.

## Como Recriar o Projeto

1.  **Clone o repositório**
    ```bash
    git clone https://github.com/seu-usuario/projeto-bi-cinema.git
    cd projeto-bi-cinema
    ```
2.  **Instale as dependências da pipeline**
    ```bash
    pip install pandas numpy openpyxl
    ```
3.  **Execute a Pipeline de Dados**
    Primeiro, gere os dados brutos:
    ```bash
    python gerar_dados_massivos.py
    ```
    Em seguida, transforme os dados para o formato de BI:
    ```bash
    python gerar_tabelas_excel.py
    ```
    Isso criará uma pasta `tabelas_powerbi` com os arquivos Excel necessários.

4.  **Carregue os dados no Power BI**
    -   Abra o Power BI Desktop.
    -   Clique em "Obter Dados" e selecione "Excel".
    -   Carregue o arquivo `cinema_bi_completo.xlsx` (ou os arquivos individuais) da pasta `tabelas_powerbi`.
    -   Na aba "Modelagem", crie os relacionamentos entre a tabela Fato e as Dimensões, conforme o modelo Star Schema.
    -   Com os dados carregados e relacionados, você pode recriar os visuais do dashboard.

## Contribuição

Este é um projeto acadêmico, mas sugestões e feedbacks são sempre bem-vindos!

1.  Faça um Fork do projeto.
2.  Crie sua Feature Branch (`git checkout -b feature/NovaAnalise`).
3.  Faça Commit de suas mudanças (`git commit -m 'Adiciona nova análise X'`).
4.  Abra um Pull Request.

## Suporte e Contato

-   **Email**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)
-   **LinkedIn**: [Gustavo Moreno](https://www.linkedin.com/in/gustavo-moreno-8a925b26a/)

## Licença

Este projeto está licenciado sob uma Licença Proprietária.

**Uso Restrito**: Este projeto foi desenvolvido para fins acadêmicos. Uso comercial ou redistribuição requer autorização expressa.

---

<div align="center">
  Desenvolvido por Gustavo Moreno
  <br><br>
  <a href="https.linkedin.com/in/gustavo-moreno-8a925b26a/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" alt="LinkedIn"/>
  </a>
</div>
