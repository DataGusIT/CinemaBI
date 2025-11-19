import pandas as pd
import os

print("Iniciando o processo de geração das tabelas para o Power BI.")
print("=" * 60)

# --- 1. Leitura e Preparação dos Arquivos de Origem ---
try:
    path = 'dados_origem'
    print(f"Lendo arquivos do diretório: '{path}'...")
    
    cinemas_df = pd.read_csv(os.path.join(path, 'cinemas.csv'), encoding='utf-8')
    diretores_df = pd.read_csv(os.path.join(path, 'diretores.csv'), encoding='utf-8')
    atores_df = pd.read_csv(os.path.join(path, 'atores.csv'), encoding='utf-8')
    filmes_df = pd.read_csv(os.path.join(path, 'filmes.csv'), encoding='utf-8')
    filmes_atores_df = pd.read_csv(os.path.join(path, 'filmes_atores.csv'), encoding='utf-8')
    sessoes_publico_df = pd.read_csv(os.path.join(path, 'sessoes_publico.csv'), encoding='utf-8')
    
    # Padroniza os nomes das colunas, removendo espaços em branco
    for df in [cinemas_df, diretores_df, atores_df, filmes_df, filmes_atores_df, sessoes_publico_df]:
        df.columns = df.columns.str.strip()

    # Garante a tipagem correta das colunas de identificação
    id_columns_map = {
        cinemas_df: ['id'],
        diretores_df: ['id'],
        atores_df: ['id'],
        filmes_df: ['id', 'diretor_id'],
        filmes_atores_df: ['filme_id', 'ator_id'],
        sessoes_publico_df: ['cinema_id', 'filme_id', 'idade_publico']
    }
    
    for df, cols in id_columns_map.items():
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    print("Arquivos CSV lidos e pré-processados com sucesso.")

except FileNotFoundError as e:
    print(f"Erro Crítico: Arquivo não encontrado. Verifique se o diretório '{path}' existe e contém os arquivos CSV necessários. Detalhe: {e}")
    exit()
except Exception as e:
    print(f"Erro Crítico durante o processamento dos arquivos CSV: {e}")
    exit()

# Função para categorizar a idade em faixas etárias
def criar_faixa_etaria(idade):
    if pd.isnull(idade):
        return 'Não informado'
    if idade <= 12: return 'Criança (0-12)'
    if idade <= 17: return 'Adolescente (13-17)'
    if idade <= 59: return 'Adulto (18-59)'
    return 'Idoso (60+)'

sessoes_publico_df['faixa_etaria'] = sessoes_publico_df['idade_publico'].apply(criar_faixa_etaria)

# --- 2. Construção das Tabelas de Dimensão ---
print("\nIniciando a criação das tabelas de dimensão...")

# Dim_Cinema
dim_cinema = cinemas_df.copy()
dim_cinema.insert(0, 'sk_cinema', range(1, len(dim_cinema) + 1))
dim_cinema = dim_cinema.rename(columns={'id': 'id_cinema_original'})
print("- Dimensão 'Dim_Cinema' criada.")

# Dim_Ator
dim_ator = atores_df[['id', 'nome', 'nacionalidade', 'sexo']].copy()
dim_ator.insert(0, 'sk_ator', range(1, len(dim_ator) + 1))
dim_ator = dim_ator.rename(columns={'id': 'id_ator_original', 'nome': 'nome_ator'})
print("- Dimensão 'Dim_Ator' criada.")

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
print("- Dimensão 'Dim_Filme' criada.")

# Dim_Tempo
sessoes_publico_df['data_exibicao'] = pd.to_datetime(sessoes_publico_df['data_exibicao'])
datas_unicas = sessoes_publico_df['data_exibicao'].unique()
dim_tempo = pd.DataFrame({'data': pd.to_datetime(datas_unicas)})
dim_tempo['sk_tempo'] = dim_tempo['data'].dt.strftime('%Y%m%d').astype(int)
dim_tempo['ano'] = dim_tempo['data'].dt.year
dim_tempo['mes_numero'] = dim_tempo['data'].dt.month
dim_tempo['mes_nome'] = dim_tempo['data'].dt.strftime('%B')
dim_tempo['dia_do_mes'] = dim_tempo['data'].dt.day
dim_tempo['dia_da_semana'] = dim_tempo['data'].dt.strftime('%A')
dim_tempo['trimestre'] = dim_tempo['data'].dt.quarter
dim_tempo['semestre'] = (dim_tempo['data'].dt.quarter > 2).astype(int) + 1
dim_tempo['flag_fim_de_semana'] = dim_tempo['data'].dt.dayofweek.isin([5, 6]).map({True: 'Sim', False: 'Não'})
dim_tempo = dim_tempo[['sk_tempo', 'data', 'ano', 'mes_numero', 'mes_nome', 'dia_do_mes', 
                        'dia_da_semana', 'trimestre', 'semestre', 'flag_fim_de_semana']]
print("- Dimensão 'Dim_Tempo' criada.")

# Dim_Publico
dim_publico = sessoes_publico_df[['sexo_publico', 'faixa_etaria']].copy()
dim_publico = dim_publico.rename(columns={'sexo_publico': 'sexo'})
dim_publico = dim_publico.drop_duplicates().reset_index(drop=True)
dim_publico.insert(0, 'sk_publico', range(1, len(dim_publico) + 1))
print("- Dimensão 'Dim_Publico' criada.")

# --- 3. Construção da Tabela Bridge ---
print("\nIniciando a criação da tabela bridge...")

# Bridge_Filme_Ator
bridge = pd.merge(filmes_atores_df, dim_filme[['sk_filme', 'id_filme_original']], 
                  left_on='filme_id', right_on='id_filme_original')
bridge = pd.merge(bridge, dim_ator[['sk_ator', 'id_ator_original']], 
                  left_on='ator_id', right_on='id_ator_original')
bridge_filme_ator = bridge[['sk_filme', 'sk_ator']].copy()
print("- Tabela 'Bridge_Filme_Ator' criada.")

# --- 4. Construção da Tabela Fato ---
print("\nIniciando a criação da tabela fato...")

# Fato_Publico
fato = sessoes_publico_df.copy()

# Junção com as chaves substitutas das dimensões
fato = pd.merge(fato, dim_filme[['sk_filme', 'id_filme_original']], 
                left_on='filme_id', right_on='id_filme_original', how='left')
fato = pd.merge(fato, dim_cinema[['sk_cinema', 'id_cinema_original']], 
                left_on='cinema_id', right_on='id_cinema_original', how='left')
fato = pd.merge(fato, dim_tempo[['sk_tempo', 'data']], 
                left_on='data_exibicao', right_on='data', how='left')
fato = pd.merge(fato, dim_publico[['sk_publico', 'sexo', 'faixa_etaria']], 
                left_on=['sexo_publico', 'faixa_etaria'], 
                right_on=['sexo', 'faixa_etaria'], how='left')

# Seleção e renomeação das colunas para a tabela fato final
fato_publico = fato[['sk_tempo', 'sk_cinema', 'sk_filme', 'sk_publico', 'idade_publico']].copy()
fato_publico = fato_publico.rename(columns={'idade_publico': 'idade_espectador'})
fato_publico['quantidade_espectadores'] = 1
print("- Tabela 'Fato_Publico' criada.")

# --- 5. Exportação dos Dados para Excel ---
output_path = 'tabelas_powerbi'
os.makedirs(output_path, exist_ok=True)

print(f"\nIniciando a exportação das tabelas para o diretório '{output_path}'...")

try:
    # Exportação para arquivos Excel individuais
    dim_cinema.to_excel(os.path.join(output_path, 'dim_cinema.xlsx'), index=False)
    dim_ator.to_excel(os.path.join(output_path, 'dim_ator.xlsx'), index=False)
    dim_filme.to_excel(os.path.join(output_path, 'dim_filme.xlsx'), index=False)
    dim_tempo.to_excel(os.path.join(output_path, 'dim_tempo.xlsx'), index=False)
    dim_publico.to_excel(os.path.join(output_path, 'dim_publico.xlsx'), index=False)
    bridge_filme_ator.to_excel(os.path.join(output_path, 'bridge_filme_ator.xlsx'), index=False)
    fato_publico.to_excel(os.path.join(output_path, 'fato_publico.xlsx'), index=False)

    print("  - Arquivos individuais salvos com sucesso.")

    # Consolidação de todas as tabelas em um único arquivo Excel
    with pd.ExcelWriter(os.path.join(output_path, 'cinema_bi_completo.xlsx'), engine='openpyxl') as writer:
        dim_cinema.to_excel(writer, sheet_name='dim_cinema', index=False)
        dim_ator.to_excel(writer, sheet_name='dim_ator', index=False)
        dim_filme.to_excel(writer, sheet_name='dim_filme', index=False)
        dim_tempo.to_excel(writer, sheet_name='dim_tempo', index=False)
        dim_publico.to_excel(writer, sheet_name='dim_publico', index=False)
        bridge_filme_ator.to_excel(writer, sheet_name='bridge_filme_ator', index=False)
        fato_publico.to_excel(writer, sheet_name='fato_publico', index=False)
    
    print("  - Arquivo consolidado 'cinema_bi_completo.xlsx' salvo com sucesso.")

except Exception as e:
    print(f"Erro Crítico durante a exportação para Excel: {e}")
    exit()

print(f"\n{'='*60}")
print(f"Processo concluído. As tabelas foram geradas no diretório: '{output_path}'")
print(f"{'='*60}")

print("\nGuia de Importação para o Power BI:")
print("1. No Power BI Desktop, selecione 'Obter Dados' e escolha 'Pasta de Trabalho do Excel'.")
print(f"2. Navegue até o diretório '{output_path}' e selecione o arquivo 'cinema_bi_completo.xlsx'.")
print("3. No navegador de arquivos, marque todas as planilhas (tabelas) e clique em 'Carregar'.")
print("4. Acesse a exibição de 'Modelo' para configurar os relacionamentos entre as tabelas:")
print("   - Conecte fato_publico[sk_cinema] a dim_cinema[sk_cinema]")
print("   - Conecte fato_publico[sk_filme] a dim_filme[sk_filme]")
print("   - Conecte fato_publico[sk_tempo] a dim_tempo[sk_tempo]")
print("   - Conecte fato_publico[sk_publico] a dim_publico[sk_publico]")
print("   - Conecte bridge_filme_ator[sk_filme] a dim_filme[sk_filme]")
print("   - Conecte bridge_filme_ator[sk_ator] a dim_ator[sk_ator]")
print("\nO modelo de dados está pronto para a criação de relatórios e dashboards.")