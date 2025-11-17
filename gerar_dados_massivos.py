import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

print("🎬 Gerador de Dados Massivos para Cinema BI")
print("=" * 60)

# Configuração: QUANTAS SESSÕES DESEJA GERAR?
NUM_SESSOES = 300  # ← ALTERE AQUI: Número de SESSÕES (não espectadores)
print(f"📊 Gerando {NUM_SESSOES} sessões de cinema...")
print(f"💡 Cada sessão terá uma ocupação realista baseada na capacidade da sala")

# --- DADOS BASE ---

# Cinemas (vamos criar mais cinemas)
cinemas = [
    {"id": 1, "nome_fantasia": "Cinépolis Central", "endereco": "Rua das Flores 123, São Paulo, SP", "capacidade": 250},
    {"id": 2, "nome_fantasia": "Cinemark Leste", "endereco": "Avenida Principal 456, Rio de Janeiro, RJ", "capacidade": 300},
    {"id": 3, "nome_fantasia": "UCI Shopping Paulista", "endereco": "Av Paulista 1000, São Paulo, SP", "capacidade": 280},
    {"id": 4, "nome_fantasia": "Kinoplex Norte", "endereco": "Shopping Norte, Brasília, DF", "capacidade": 200},
    {"id": 5, "nome_fantasia": "Cinesystem Sul", "endereco": "Av Getúlio Vargas 789, Porto Alegre, RS", "capacidade": 220},
]

# Diretores
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

# Atores
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

# Filmes
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

# Filmes e Atores (relacionamento)
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

# --- GERAÇÃO DE SESSÕES MASSIVAS COM OCUPAÇÃO REALISTA ---

# Período: últimos 6 meses
data_inicio = datetime(2024, 5, 1)
data_fim = datetime(2024, 10, 31)
dias_range = (data_fim - data_inicio).days

sessoes = []
id_espectador = 1000

print(f"📽️  Criando {NUM_SESSOES} sessões com ocupação realista de cinema...")

# Dicionário para buscar capacidade do cinema
cinemas_dict = {c['id']: c for c in cinemas}

for sessao_num in range(NUM_SESSOES):
    # Dados da sessão
    sessao_id = f"S{1000 + sessao_num}"
    cinema_id = random.choice([c['id'] for c in cinemas])
    filme_id = random.choice([f['id'] for f in filmes])
    
    # Data aleatória no período
    dias_offset = random.randint(0, dias_range)
    data_exibicao = data_inicio + timedelta(days=dias_offset)
    
    # Dia da semana influencia ocupação
    dia_semana = data_exibicao.weekday()
    is_fim_de_semana = dia_semana >= 5  # Sábado ou Domingo
    is_sexta = dia_semana == 4
    
    # Capacidade da sala
    capacidade_sala = cinemas_dict[cinema_id]['capacidade']
    
    # Taxa de ocupação realista baseada no dia
    if is_fim_de_semana:
        # Fim de semana: 60% a 95% de ocupação
        taxa_ocupacao = random.uniform(0.60, 0.95)
    elif is_sexta:
        # Sexta-feira: 50% a 85% de ocupação
        taxa_ocupacao = random.uniform(0.50, 0.85)
    else:
        # Dias úteis: 15% a 60% de ocupação
        taxa_ocupacao = random.uniform(0.15, 0.60)
    
    # Blockbusters têm mais público
    filmes_populares = [1, 2, 3, 5]  # Oppenheimer, Dune, Barbie, Avatar
    if filme_id in filmes_populares:
        taxa_ocupacao = min(taxa_ocupacao * 1.3, 0.98)
    
    # Número de espectadores nesta sessão
    num_espectadores_sessao = int(capacidade_sala * taxa_ocupacao)
    num_espectadores_sessao = max(5, num_espectadores_sessao)  # Mínimo 5 pessoas
    
    # Gera os espectadores desta sessão
    for _ in range(num_espectadores_sessao):
        # Perfil do público (mais realista)
        # Fim de semana tem mais famílias (mais crianças)
        if is_fim_de_semana:
            tipo_publico = random.choices(
                ['adulto', 'adolescente', 'crianca', 'idoso'],
                weights=[50, 20, 25, 5]  # Mais crianças no FDS
            )[0]
        else:
            tipo_publico = random.choices(
                ['adulto', 'adolescente', 'crianca', 'idoso'],
                weights=[65, 20, 10, 5]  # Mais adultos em dias úteis
            )[0]
        
        if tipo_publico == 'adulto':
            idade = random.randint(18, 59)
        elif tipo_publico == 'adolescente':
            idade = random.randint(13, 17)
        elif tipo_publico == 'crianca':
            idade = random.randint(5, 12)
        else:  # idoso
            idade = random.randint(60, 85)
        
        # Sexo com distribuição aproximada 50/50
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

print(f"✅ {len(sessoes)} sessões geradas!")

# --- SALVAR CSVs ---

output_path = 'dados_origem'
os.makedirs(output_path, exist_ok=True)

# Salva cada tabela
pd.DataFrame(cinemas).to_csv(os.path.join(output_path, 'cinemas.csv'), index=False, encoding='utf-8')
pd.DataFrame(diretores).to_csv(os.path.join(output_path, 'diretores.csv'), index=False, encoding='utf-8')
pd.DataFrame(atores).to_csv(os.path.join(output_path, 'atores.csv'), index=False, encoding='utf-8')
pd.DataFrame(filmes).to_csv(os.path.join(output_path, 'filmes.csv'), index=False, encoding='utf-8')
pd.DataFrame(filmes_atores).to_csv(os.path.join(output_path, 'filmes_atores.csv'), index=False, encoding='utf-8')
pd.DataFrame(sessoes).to_csv(os.path.join(output_path, 'sessoes_publico.csv'), index=False, encoding='utf-8')

print(f"\n💾 Arquivos salvos na pasta '{output_path}':")
print(f"  ✓ cinemas.csv ({len(cinemas)} registros)")
print(f"  ✓ diretores.csv ({len(diretores)} registros)")
print(f"  ✓ atores.csv ({len(atores)} registros)")
print(f"  ✓ filmes.csv ({len(filmes)} registros)")
print(f"  ✓ filmes_atores.csv ({len(filmes_atores)} registros)")
print(f"  ✓ sessoes_publico.csv ({len(sessoes)} registros)")

print("\n" + "=" * 60)
print("🚀 PRÓXIMOS PASSOS:")
print("1. Execute: python gerar_tabelas_excel.py")
print("2. No Power BI: Dados → Atualizar Tudo (ou clique com botão direito na tabela → Atualizar)")
print("3. Pronto! Os novos dados aparecerão automaticamente!")
print("=" * 60)

# Estatísticas
print("\n📊 ESTATÍSTICAS DOS DADOS GERADOS:")
print(f"  • Total de espectadores: {len(sessoes):,}")
print(f"  • Total de sessões únicas: {NUM_SESSOES}")
print(f"  • Média de espectadores por sessão: {len(sessoes)/NUM_SESSOES:.1f}")
print(f"  • Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
print(f"  • Cinemas: {len(cinemas)}")
print(f"  • Filmes: {len(filmes)}")
print(f"  • Atores: {len(atores)}")

df_sessoes = pd.DataFrame(sessoes)
print(f"\n  📊 Ocupação por Cinema:")
for cinema in cinemas:
    cinema_sessoes = df_sessoes[df_sessoes['cinema_id'] == cinema['id']]
    if len(cinema_sessoes) > 0:
        sessoes_cinema = cinema_sessoes['sessao_id'].nunique()
        espectadores_cinema = len(cinema_sessoes)
        media_ocupacao = espectadores_cinema / sessoes_cinema if sessoes_cinema > 0 else 0
        taxa_ocupacao = (media_ocupacao / cinema['capacidade']) * 100
        print(f"    {cinema['nome_fantasia']}: {espectadores_cinema:,} espectadores em {sessoes_cinema} sessões")
        print(f"      → Média: {media_ocupacao:.1f} pessoas/sessão ({taxa_ocupacao:.1f}% de ocupação)")

print(f"\n  👥 Distribuição por sexo:")
print(f"    - Masculino: {len(df_sessoes[df_sessoes['sexo_publico']=='Masculino']):,} ({len(df_sessoes[df_sessoes['sexo_publico']=='Masculino'])/len(df_sessoes)*100:.1f}%)")
print(f"    - Feminino: {len(df_sessoes[df_sessoes['sexo_publico']=='Feminino']):,} ({len(df_sessoes[df_sessoes['sexo_publico']=='Feminino'])/len(df_sessoes)*100:.1f}%)")
print(f"  • Idade média: {df_sessoes['idade_publico'].mean():.1f} anos")