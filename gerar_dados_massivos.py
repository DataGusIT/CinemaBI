import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

print("Gerador de Dados Massivos para Business Intelligence de Cinema")
print("=" * 60)

# Parâmetro de configuração para o número de sessões a serem geradas
NUM_SESSOES = 300  # Altere este valor para definir o número de sessões
print(f"Gerando {NUM_SESSOES} sessões de cinema...")
print(f"A ocupação de cada sessão será calculada com base na capacidade da sala e no dia da semana.")

# --- Definição dos dados base ---

# Lista de cinemas com seus respectivos detalhes
cinemas = [
    {"id": 1, "nome_fantasia": "Cinépolis Central", "endereco": "Rua das Flores 123, São Paulo, SP", "capacidade": 250},
    {"id": 2, "nome_fantasia": "Cinemark Leste", "endereco": "Avenida Principal 456, Rio de Janeiro, RJ", "capacidade": 300},
    {"id": 3, "nome_fantasia": "UCI Shopping Paulista", "endereco": "Av Paulista 1000, São Paulo, SP", "capacidade": 280},
    {"id": 4, "nome_fantasia": "Kinoplex Norte", "endereco": "Shopping Norte, Brasília, DF", "capacidade": 200},
    {"id": 5, "nome_fantasia": "Cinesystem Sul", "endereco": "Av Getúlio Vargas 789, Porto Alegre, RS", "capacidade": 220},
]

# Lista de diretores
diretores = [
    {"id": 101, "nome": "Christopher Nolan"},
    {"id": 102, "nome": "Denis Villeneuve"},
    {"id": 103, "nome": "Greta Gerwig"},
    {"id": 104, "nome": "Martin Scorsese"},
    {"id": 105, "nome": "Steven Spielberg"},
    {"id": 106, "nome": "Quentin Tarantino"},
    {"id": 107, "nome": "James Cameron"},
    {"id": 108, "nome": "Ridley Scott"},
]

# Lista de atores com detalhes demográficos
atores = [
    {"id": 201, "nome": "Cillian Murphy", "nacionalidade": "Irlandesa", "sexo": "Masculino", "idade": 48},
    {"id": 202, "nome": "Timothée Chalamet", "nacionalidade": "Americana", "sexo": "Masculino", "idade": 28},
    {"id": 203, "nome": "Zendaya", "nacionalidade": "Americana", "sexo": "Feminino", "idade": 28},
    {"id": 204, "nome": "Margot Robbie", "nacionalidade": "Australiana", "sexo": "Feminino", "idade": 34},
    {"id": 205, "nome": "Ryan Gosling", "nacionalidade": "Canadense", "sexo": "Masculino", "idade": 44},
    {"id": 206, "nome": "Leonardo DiCaprio", "nacionalidade": "Americana", "sexo": "Masculino", "idade": 49},
    {"id": 207, "nome": "Scarlett Johansson", "nacionalidade": "Americana", "sexo": "Feminino", "idade": 39},
    {"id": 208, "nome": "Tom Hanks", "nacionalidade": "Americana", "sexo": "Masculino", "idade": 67},
    {"id": 209, "nome": "Emma Stone", "nacionalidade": "Americana", "sexo": "Feminino", "idade": 35},
    {"id": 210, "nome": "Brad Pitt", "nacionalidade": "Americana", "sexo": "Masculino", "idade": 60},
]

# Lista de filmes com metadados
filmes = [
    {"id": 1, "titulo_original": "Oppenheimer", "titulo_portugues": "Oppenheimer", "genero": "Drama", "duracao": 180, "impropriedade": "16 anos", "pais_origem": "EUA", "diretor_id": 101},
    {"id": 2, "titulo_original": "Dune: Part Two", "titulo_portugues": "Duna: Parte Dois", "genero": "Ficção Científica", "duracao": 166, "impropriedade": "14 anos", "pais_origem": "EUA", "diretor_id": 102},
    {"id": 3, "titulo_original": "Barbie", "titulo_portugues": "Barbie", "genero": "Comédia", "duracao": 114, "impropriedade": "12 anos", "pais_origem": "EUA", "diretor_id": 103},
    {"id": 4, "titulo_original": "The Killer", "titulo_portugues": "O Assassino", "genero": "Ação", "duracao": 118, "impropriedade": "18 anos", "pais_origem": "EUA", "diretor_id": 104},
    {"id": 5, "titulo_original": "Avatar 3", "titulo_portugues": "Avatar: O Caminho da Água", "genero": "Ficção Científica", "duracao": 192, "impropriedade": "12 anos", "pais_origem": "EUA", "diretor_id": 107},
    {"id": 6, "titulo_original": "Napoleon", "titulo_portugues": "Napoleão", "genero": "Drama", "duracao": 158, "impropriedade": "16 anos", "pais_origem": "EUA", "diretor_id": 108},
    {"id": 7, "titulo_original": "Wonka", "titulo_portugues": "Wonka", "genero": "Fantasia", "duracao": 116, "impropriedade": "Livre", "pais_origem": "EUA", "diretor_id": 105},
    {"id": 8, "titulo_original": "The Equalizer 3", "titulo_portugues": "O Protetor 3", "genero": "Ação", "duracao": 109, "impropriedade": "18 anos", "pais_origem": "EUA", "diretor_id": 106},
]

# Tabela de relacionamento entre filmes e atores
filmes_atores = [
    {"filme_id": 1, "ator_id": 201},
    {"filme_id": 2, "ator_id": 202}, {"filme_id": 2, "ator_id": 203},
    {"filme_id": 3, "ator_id": 204}, {"filme_id": 3, "ator_id": 205},
    {"filme_id": 4, "ator_id": 206},
    {"filme_id": 5, "ator_id": 207}, {"filme_id": 5, "ator_id": 209},
    {"filme_id": 6, "ator_id": 206},
    {"filme_id": 7, "ator_id": 202},
    {"filme_id": 8, "ator_id": 210},
]

# --- Geração de dados de sessões com ocupação realista ---

# Define o período de geração dos dados
data_inicio = datetime(2024, 5, 1)
data_fim = datetime(2024, 10, 31)
dias_range = (data_fim - data_inicio).days

sessoes = []
id_espectador = 1000

print(f"Iniciando a criação de {NUM_SESSOES} sessões com dados de público...")

# Mapeia IDs de cinema para suas capacidades para acesso rápido
cinemas_dict = {c['id']: c for c in cinemas}

for sessao_num in range(NUM_SESSOES):
    # Seleciona aleatoriamente os dados da sessão
    sessao_id = f"S{1000 + sessao_num}"
    cinema_id = random.choice([c['id'] for c in cinemas])
    filme_id = random.choice([f['id'] for f in filmes])
    
    # Define uma data aleatória dentro do período especificado
    dias_offset = random.randint(0, dias_range)
    data_exibicao = data_inicio + timedelta(days=dias_offset)
    
    # O dia da semana influencia a taxa de ocupação
    dia_semana = data_exibicao.weekday()
    is_fim_de_semana = dia_semana >= 5  # Sábado (5) ou Domingo (6)
    is_sexta = dia_semana == 4
    
    # Obtém a capacidade da sala do cinema selecionado
    capacidade_sala = cinemas_dict[cinema_id]['capacidade']
    
    # Define uma taxa de ocupação realista com base no dia da semana
    if is_fim_de_semana:
        # Fim de semana tem maior ocupação: 60% a 95%
        taxa_ocupacao = random.uniform(0.60, 0.95)
    elif is_sexta:
        # Sexta-feira tem ocupação intermediária: 50% a 85%
        taxa_ocupacao = random.uniform(0.50, 0.85)
    else:
        # Dias de semana têm menor ocupação: 15% a 60%
        taxa_ocupacao = random.uniform(0.15, 0.60)
    
    # Aumenta a taxa de ocupação para filmes mais populares (blockbusters)
    filmes_populares = [1, 2, 3, 5]  # Oppenheimer, Dune, Barbie, Avatar
    if filme_id in filmes_populares:
        taxa_ocupacao = min(taxa_ocupacao * 1.3, 0.98) # Limita em 98% para não exceder a capacidade
    
    # Calcula o número de espectadores para a sessão
    num_espectadores_sessao = int(capacidade_sala * taxa_ocupacao)
    num_espectadores_sessao = max(5, num_espectadores_sessao)  # Garante um número mínimo de 5 espectadores
    
    # Gera os registros de espectadores para esta sessão
    for _ in range(num_espectadores_sessao):
        # Define o perfil do público com base no dia da semana
        # Fins de semana tendem a ter mais famílias e crianças
        if is_fim_de_semana:
            tipo_publico = random.choices(
                ['adulto', 'adolescente', 'crianca', 'idoso'],
                weights=[50, 20, 25, 5]
            )[0]
        else:
            tipo_publico = random.choices(
                ['adulto', 'adolescente', 'crianca', 'idoso'],
                weights=[65, 20, 10, 5]
            )[0]
        
        # Atribui uma idade com base no perfil do público
        if tipo_publico == 'adulto':
            idade = random.randint(18, 59)
        elif tipo_publico == 'adolescente':
            idade = random.randint(13, 17)
        elif tipo_publico == 'crianca':
            idade = random.randint(5, 12)
        else:  # idoso
            idade = random.randint(60, 85)
        
        # Distribui o sexo de forma aproximadamente igual
        sexo = random.choice(['Masculino', 'Feminino'])
        
        sessoes.append({
            "sessao_id": sessao_id,
            "cinema_id": cinema_id,
            "filme_id": filme_id,
            "data_exibicao": data_exibicao.strftime('%Y-%m-%d'),
            "sexo_publico": sexo,
            "idade_publico": idade
        })
        
        id_espectador += 1

print(f"Geração concluída: {len(sessoes)} registros de espectadores criados.")

# --- Armazenamento dos dados em arquivos CSV ---

output_path = 'dados_origem'
os.makedirs(output_path, exist_ok=True)

# Salva cada DataFrame em um arquivo CSV separado
pd.DataFrame(cinemas).to_csv(os.path.join(output_path, 'cinemas.csv'), index=False, encoding='utf-8')
pd.DataFrame(diretores).to_csv(os.path.join(output_path, 'diretores.csv'), index=False, encoding='utf-8')
pd.DataFrame(atores).to_csv(os.path.join(output_path, 'atores.csv'), index=False, encoding='utf-8')
pd.DataFrame(filmes).to_csv(os.path.join(output_path, 'filmes.csv'), index=False, encoding='utf-8')
pd.DataFrame(filmes_atores).to_csv(os.path.join(output_path, 'filmes_atores.csv'), index=False, encoding='utf-8')
pd.DataFrame(sessoes).to_csv(os.path.join(output_path, 'sessoes_publico.csv'), index=False, encoding='utf-8')

print(f"\nArquivos CSV salvos no diretório '{output_path}':")
print(f"  - cinemas.csv ({len(cinemas)} registros)")
print(f"  - diretores.csv ({len(diretores)} registros)")
print(f"  - atores.csv ({len(atores)} registros)")
print(f"  - filmes.csv ({len(filmes)} registros)")
print(f"  - filmes_atores.csv ({len(filmes_atores)} registros)")
print(f"  - sessoes_publico.csv ({len(sessoes)} registros)")

print("\n" + "=" * 60)
print("Instruções para próximos passos:")
print("1. Execute o script 'gerar_tabelas_excel.py' para consolidar os dados.")
print("2. No Power BI, utilize a função 'Atualizar Tudo' para carregar os novos dados.")
print("3. Os dashboards serão atualizados automaticamente com as novas informações.")
print("=" * 60)

# --- Exibição de estatísticas dos dados gerados ---
print("\nEstatísticas dos Dados Gerados:")
print(f"  - Total de espectadores: {len(sessoes):,}")
print(f"  - Total de sessões únicas: {NUM_SESSOES}")
print(f"  - Média de espectadores por sessão: {len(sessoes)/NUM_SESSOES:.1f}")
print(f"  - Período considerado: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
print(f"  - Quantidade de cinemas: {len(cinemas)}")
print(f"  - Quantidade de filmes: {len(filmes)}")
print(f"  - Quantidade de atores: {len(atores)}")

df_sessoes = pd.DataFrame(sessoes)
print(f"\nOcupação por Cinema:")
for cinema in cinemas:
    cinema_sessoes = df_sessoes[df_sessoes['cinema_id'] == cinema['id']]
    if not cinema_sessoes.empty:
        sessoes_cinema = cinema_sessoes['sessao_id'].nunique()
        espectadores_cinema = len(cinema_sessoes)
        media_ocupacao = espectadores_cinema / sessoes_cinema if sessoes_cinema > 0 else 0
        taxa_ocupacao_percentual = (media_ocupacao / cinema['capacidade']) * 100
        print(f"  - {cinema['nome_fantasia']}: {espectadores_cinema:,} espectadores em {sessoes_cinema} sessões")
        print(f"    Média: {media_ocupacao:.1f} pessoas/sessão (Taxa de ocupação de {taxa_ocupacao_percentual:.1f}%)")

print(f"\nDistribuição por sexo do público:")
total_espectadores = len(df_sessoes)
masculino_count = len(df_sessoes[df_sessoes['sexo_publico'] == 'Masculino'])
feminino_count = len(df_sessoes[df_sessoes['sexo_publico'] == 'Feminino'])
print(f"  - Masculino: {masculino_count:,} ({masculino_count / total_espectadores:.1%})")
print(f"  - Feminino: {feminino_count:,} ({feminino_count / total_espectadores:.1%})")
print(f"  - Idade média do público: {df_sessoes['idade_publico'].mean():.1f} anos")