import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.markdown("<h1 style='text-align: center; color: black;'>💸 DiviDash - Oficial 💸</h1>", unsafe_allow_html=True)

# Estilo personalizado para o fundo, os cards e o gráfico
st.markdown(
    """
    <style>
    body {
        background-color: #d0d2d6;
        color: black;  /* Definindo a cor do texto para preto */
    }
    .stApp {
        background-color: #d0d2d6;
        color: black;  /* Definindo a cor do texto para preto */
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 150px;  /* Altura fixa para todos os cards */
        box-sizing: border-box;  /* Inclui padding e bordas no cálculo da largura */
        overflow: hidden;  /* Oculta o conteúdo que excede a altura do card */
    }
    .card h2 {
        font-size: 18px;  /* Tamanho do título reduzido */
        margin-bottom: 10px;
    }
    .card p {
        font-size: 24px;  /* Tamanho do valor aumentado */
        margin: 0;
    }
    .card p.delta {
        font-size: 18px;  /* Tamanho do valor delta ajustado */
        color: green;  /* Cor verde para o texto delta */
    }
    .card-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;  /* Espaço entre os cartões e o gráfico */
    }
    .card-container .card {
        flex: 1;
        margin: 0 10px;  /* Espaço entre os cartões */
    }
    .chart-container {
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        overflow: hidden;  /* Garante que o gráfico não ultrapasse o contêiner */
        padding: 20px;  /* Opcional: adicione padding se desejar espaçamento interno */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar o dataframe
df = pd.read_excel('dividendos.xlsx')

# Convert 'Data' column to datetime
df['Ref'] = pd.to_datetime(df['Ref'])

# Extract only the date part
df['Ref'] = df['Ref'].dt.date

df = df.sort_values('Ref')

df['mes'] = df['Ref'].apply(lambda x: f"{x.year}-{str(x.month).zfill(2)}")

# Adiciona o título do painel de filtros
st.sidebar.title("Filtros")

# Adiciona "Todos" como a primeira opção nas listas de filtros
Fundos = ['Todos'] + df['FII'].unique().tolist()

Fundo = st.sidebar.selectbox("Fundo", Fundos)

# Filtra o dataframe com base na categoria, integrante e unidade selecionados, se "Todos" não estiver selecionado
df_filtered = df.copy()

if Fundo != 'Todos':
    df_filtered = df_filtered[df_filtered['FII'] == Fundo]

df_filtered = df_filtered.reset_index(drop=True)

# Agrupa os dados por mês e soma os dividendos
df_grouped = df_filtered.groupby(['mes'])[['Dividendo']].sum().reset_index()

# Obter o valor dos dividendos do último mês disponível
last_month_value = df_grouped['Dividendo'].iloc[-1]

# Definir a meta
target_value = 500

# Calcular a distância até a meta e a porcentagem do objetivo alcançado
distance_to_target = target_value - float(last_month_value)
percentage_achieved = (float(last_month_value) / target_value) * 100

# Exibir os cartões com as informações acima do gráfico
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="card">
            <h2>Dividendos (Último Mês)</h2>
            <p>R$ {last_month_value}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card">
            <h2>Meta</h2>
            <p>R$ 500</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card">
            <h2>Distância até a Meta</h2>
            <p>R$ {distance_to_target:.0f}</p>
            <p class="delta">(<span style="color: green;">{percentage_achieved:.2f}% do objetivo alcançado</span>)</p>
        </div>
    """, unsafe_allow_html=True)

# Formata os valores de 'Dividendo' sem casas decimais
df_grouped['Dividendo'] = df_grouped['Dividendo'].apply(lambda x: f"{x:.0f}")

# Criar containers para os gráficos
container1 = st.container()
container2 = st.container()
container3 = st.container()

# Cria o gráfico de linha com anotações
fig = px.line(df_grouped, x='mes', y='Dividendo', title='Evolução dos Dividendos ao Longo do Tempo',
              labels={'mes': 'Mês', 'Dividendo': 'Dividendo (R$)'}, text='Dividendo')

# Centraliza o título do gráfico
fig.update_layout(title={'text': 'Evolução dos Dividendos ao Longo do Tempo', 'x':0.5, 'xanchor': 'center'})

# Atualiza a posição do texto para que apareça no centro das marcas de dados
fig.update_traces(textposition='top right')

# Exibe o gráfico no container com a borda e sombra
with container1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Função para definir a cor das barras
def color_bars(values):
    colors = []
    for value in values:
        if value == max(values):
            colors.append('#53c654')  # Maior valor em verde
        elif value == min(values):
            colors.append('#940e0a')  # Menor valor em vermelho
        else:
            colors.append('#767bb2')  # Outros valores em azul
    return colors

# Exemplo de uso da função de cor das barras (você pode usar essa função para outros gráficos de barra, se necessário)
# values = df_grouped['Dividendo']
# colors = color_bars(values)
# fig.update_traces(marker=dict(color=colors))
    