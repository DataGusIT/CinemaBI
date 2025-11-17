import pandas as pd
import os

print("Iniciando geração das tabelas para Power BI...")

# --- 1. LEITURA DOS CSVS ORIGINAIS ---
try:
    path = 'dados_origem'
    cinemas_df = pd.read_csv(os.path.join(path, 'cinemas.csv'), encoding='utf-8')
    diretores_df = pd.read_csv(os.path.join(path, 'diretores.csv'), encoding='utf-8')
    atores_df = pd.read_csv(os.path.join(path, 'atores.csv'), encoding='utf-8')
    filmes_df = pd.read_csv(os.path.join(path, 'filmes.csv'), encoding='utf-8')
    filmes_atores_df = pd.read_csv(os.path.join(path, 'filmes_atores.csv'), encoding='utf-8')
    sessoes_publico_df = pd.read_csv(os.path.join(path, 'sessoes_publico.csv'), encoding='utf-8')
    
    # IMPORTANTE: Remove espaços dos nomes das colunas
    cinemas_df.columns = cinemas_df.columns.str.strip()
    diretores_df.columns = diretores_df.columns.str.strip()
    atores_df.columns = atores_df.columns.str.strip()
    filmes_df.columns = filmes_df.columns.str.strip()
    filmes_atores_df.columns = filmes_atores_df.columns.str.strip()
    sessoes_publico_df.columns = sessoes_publico_df.columns.str.strip()
    
    # Converte todos os IDs para inteiro
    if 'id' in cinemas_df.columns:
        cinemas_df['id'] = pd.to_numeric(cinemas_df['id'], errors='coerce').astype('Int64')
    if 'id' in atores_df.columns:
        atores_df['id'] = pd.to_numeric(atores_df['id'], errors='coerce').astype('Int64')
    if 'id' in filmes_df.columns:
        filmes_df['id'] = pd.to_numeric(filmes_df['id'], errors='coerce').astype('Int64')
    if 'diretor_id' in filmes_df.columns:
        filmes_df['diretor_id'] = pd.to_numeric(filmes_df['diretor_id'], errors='coerce').astype('Int64')
    if 'id' in diretores_df.columns:
        diretores_df['id'] = pd.to_numeric(diretores_df['id'], errors='coerce').astype('Int64')
    if 'filme_id' in filmes_atores_df.columns:
        filmes_atores_df['filme_id'] = pd.to_numeric(filmes_atores_df['filme_id'], errors='coerce').astype('Int64')
    if 'ator_id' in filmes_atores_df.columns:
        filmes_atores_df['ator_id'] = pd.to_numeric(filmes_atores_df['ator_id'], errors='coerce').astype('Int64')
    if 'cinema_id' in sessoes_publico_df.columns:
        sessoes_publico_df['cinema_id'] = pd.to_numeric(sessoes_publico_df['cinema_id'], errors='coerce').astype('Int64')
    if 'filme_id' in sessoes_publico_df.columns:
        sessoes_publico_df['filme_id'] = pd.to_numeric(sessoes_publico_df['filme_id'], errors='coerce').astype('Int64')
    if 'idade_publico' in sessoes_publico_df.columns:
        sessoes_publico_df['idade_publico'] = pd.to_numeric(sessoes_publico_df['idade_publico'], errors='coerce').astype('Int64')
    
    print("✓ CSVs lidos com sucesso")
except FileNotFoundError as e:
    print(f"Erro: {e}")
    exit()
except Exception as e:
    print(f"Erro ao processar CSVs: {e}")
    print("Verificando colunas dos arquivos:")
    print(f"  cinemas.csv: {list(cinemas_df.columns)}")
    print(f"  sessoes_publico.csv: {list(sessoes_publico_df.columns)}")
    exit()

# Função para criar faixa etária
def criar_faixa_etaria(idade):
    if idade <= 12: return 'Criança (0-12)'
    if idade <= 17: return 'Adolescente (13-17)'
    if idade <= 59: return 'Adulto (18-59)'
    return 'Idoso (60+)'

sessoes_publico_df['faixa_etaria'] = sessoes_publico_df['idade_publico'].apply(criar_faixa_etaria)

# --- 2. CRIAÇÃO DAS DIMENSÕES ---

# Dim_Cinema
dim_cinema = cinemas_df.copy()
dim_cinema.insert(0, 'sk_cinema', range(1, len(dim_cinema) + 1))
dim_cinema = dim_cinema.rename(columns={'id': 'id_cinema_original'})
print("✓ Dim_Cinema criada")

# Dim_Ator
dim_ator = atores_df[['id', 'nome', 'nacionalidade', 'sexo']].copy()
dim_ator.insert(0, 'sk_ator', range(1, len(dim_ator) + 1))
dim_ator = dim_ator.rename(columns={'id': 'id_ator_original', 'nome': 'nome_ator'})
print("✓ Dim_Ator criada")

# Dim_Filme
filmes_com_diretor = pd.merge(filmes_df, diretores_df, left_on='diretor_id', right_on='id', how='left')
dim_filme = filmes_com_diretor[['id_x', 'titulo_original', 'titulo_portugues', 'genero', 
                                  'duracao', 'impropriedade', 'pais_origem', 'nome']].copy()
dim_filme.insert(0, 'sk_filme', range(1, len(dim_filme) + 1))
dim_filme = dim_filme.rename(columns={
    'id_x': 'id_filme_original',
    'duracao': 'duracao_minutos',
    'impropriedade': 'faixa_etaria_impropriedade',
    'nome': 'nome_diretor'
})
print("✓ Dim_Filme criada")

# Dim_Tempo
sessoes_publico_df['data_exibicao'] = pd.to_datetime(sessoes_publico_df['data_exibicao'])
datas = sessoes_publico_df['data_exibicao'].unique()
dim_tempo = pd.DataFrame({'data': pd.to_datetime(datas)})
dim_tempo['sk_tempo'] = dim_tempo['data'].dt.strftime('%Y%m%d').astype(int)
dim_tempo['ano'] = dim_tempo['data'].dt.year
dim_tempo['mes_numero'] = dim_tempo['data'].dt.month
dim_tempo['mes_nome'] = dim_tempo['data'].dt.month_name()
dim_tempo['dia_do_mes'] = dim_tempo['data'].dt.day
dim_tempo['dia_da_semana'] = dim_tempo['data'].dt.day_name()
dim_tempo['trimestre'] = dim_tempo['data'].dt.quarter
dim_tempo['semestre'] = (dim_tempo['data'].dt.quarter > 2).astype(int) + 1
dim_tempo['flag_fim_de_semana'] = dim_tempo['data'].dt.dayofweek.isin([5, 6]).map({True: 'Sim', False: 'Não'})
dim_tempo = dim_tempo[['sk_tempo', 'data', 'ano', 'mes_numero', 'mes_nome', 'dia_do_mes', 
                        'dia_da_semana', 'trimestre', 'semestre', 'flag_fim_de_semana']]
print("✓ Dim_Tempo criada")

# Dim_Publico
dim_publico = sessoes_publico_df[['sexo_publico', 'faixa_etaria']].copy()
dim_publico = dim_publico.rename(columns={'sexo_publico': 'sexo'})
dim_publico = dim_publico.drop_duplicates().reset_index(drop=True)
dim_publico.insert(0, 'sk_publico', range(1, len(dim_publico) + 1))
print("✓ Dim_Publico criada")

# --- 3. CRIAÇÃO DA BRIDGE ---

# Bridge_Filme_Ator
bridge = pd.merge(filmes_atores_df, dim_filme[['sk_filme', 'id_filme_original']], 
                  left_on='filme_id', right_on='id_filme_original')
bridge = pd.merge(bridge, dim_ator[['sk_ator', 'id_ator_original']], 
                  left_on='ator_id', right_on='id_ator_original')
bridge_filme_ator = bridge[['sk_filme', 'sk_ator']].copy()
print("✓ Bridge_Filme_Ator criada")

# --- 4. CRIAÇÃO DA FATO ---

# Fato_Publico
fato = sessoes_publico_df.copy()

# Merge com dim_filme
fato = pd.merge(fato, dim_filme[['sk_filme', 'id_filme_original']], 
                left_on='filme_id', right_on='id_filme_original', how='left')

# Merge com dim_cinema
fato = pd.merge(fato, dim_cinema[['sk_cinema', 'id_cinema_original']], 
                left_on='cinema_id', right_on='id_cinema_original', how='left')

# Merge com dim_tempo
fato = pd.merge(fato, dim_tempo[['sk_tempo', 'data']], 
                left_on='data_exibicao', right_on='data', how='left')

# Merge com dim_publico
fato = pd.merge(fato, dim_publico[['sk_publico', 'sexo', 'faixa_etaria']], 
                left_on=['sexo_publico', 'faixa_etaria'], 
                right_on=['sexo', 'faixa_etaria'], how='left')

# Seleciona apenas as colunas necessárias
fato_publico = fato[['sk_tempo', 'sk_cinema', 'sk_filme', 'sk_publico', 'idade_publico']].copy()
fato_publico = fato_publico.rename(columns={'idade_publico': 'idade_espectador'})
fato_publico['quantidade_espectadores'] = 1

print("✓ Fato_Publico criada")

# --- 5. SALVAR EM EXCEL ---

# Cria pasta de saída se não existir
output_path = 'tabelas_powerbi'
os.makedirs(output_path, exist_ok=True)

print("\nSalvando tabelas em Excel...")

# Salva cada tabela em um arquivo Excel separado
dim_cinema.to_excel(os.path.join(output_path, 'dim_cinema.xlsx'), index=False)
print("  ✓ dim_cinema.xlsx")

dim_ator.to_excel(os.path.join(output_path, 'dim_ator.xlsx'), index=False)
print("  ✓ dim_ator.xlsx")

dim_filme.to_excel(os.path.join(output_path, 'dim_filme.xlsx'), index=False)
print("  ✓ dim_filme.xlsx")

dim_tempo.to_excel(os.path.join(output_path, 'dim_tempo.xlsx'), index=False)
print("  ✓ dim_tempo.xlsx")

dim_publico.to_excel(os.path.join(output_path, 'dim_publico.xlsx'), index=False)
print("  ✓ dim_publico.xlsx")

bridge_filme_ator.to_excel(os.path.join(output_path, 'bridge_filme_ator.xlsx'), index=False)
print("  ✓ bridge_filme_ator.xlsx")

fato_publico.to_excel(os.path.join(output_path, 'fato_publico.xlsx'), index=False)
print("  ✓ fato_publico.xlsx")

# BONUS: Salva também tudo em um único arquivo com múltiplas abas
with pd.ExcelWriter(os.path.join(output_path, 'cinema_bi_completo.xlsx'), engine='openpyxl') as writer:
    dim_cinema.to_excel(writer, sheet_name='dim_cinema', index=False)
    dim_ator.to_excel(writer, sheet_name='dim_ator', index=False)
    dim_filme.to_excel(writer, sheet_name='dim_filme', index=False)
    dim_tempo.to_excel(writer, sheet_name='dim_tempo', index=False)
    dim_publico.to_excel(writer, sheet_name='dim_publico', index=False)
    bridge_filme_ator.to_excel(writer, sheet_name='bridge_filme_ator', index=False)
    fato_publico.to_excel(writer, sheet_name='fato_publico', index=False)

print("  ✓ cinema_bi_completo.xlsx (arquivo único com todas as tabelas)")

print(f"\n{'='*60}")
print("✅ SUCESSO! Tabelas geradas na pasta '{}'".format(output_path))
print(f"{'='*60}")
print("\nPróximos passos no Power BI:")
print("1. Abra o Power BI Desktop")
print("2. Clique em 'Obter Dados' > 'Excel'")
print("3. Selecione o arquivo 'cinema_bi_completo.xlsx'")
print("4. Marque todas as planilhas e clique em 'Carregar'")
print("5. Vá em 'Modelagem' e crie os relacionamentos:")
print("   - fato_publico[sk_cinema] → dim_cinema[sk_cinema]")
print("   - fato_publico[sk_filme] → dim_filme[sk_filme]")
print("   - fato_publico[sk_tempo] → dim_tempo[sk_tempo]")
print("   - fato_publico[sk_publico] → dim_publico[sk_publico]")
print("   - bridge_filme_ator[sk_filme] → dim_filme[sk_filme]")
print("   - bridge_filme_ator[sk_ator] → dim_ator[sk_ator]")
print("\nPronto para criar seu dashboard! 📊")