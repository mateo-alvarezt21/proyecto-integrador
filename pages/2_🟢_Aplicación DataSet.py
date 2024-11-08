import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(layout="wide")

st.title("Análisis Avanzado de Composición de Campeones y Estrategias de Ban")

# Cargar datasets
match_info_df = pd.read_csv('archive/matchinfo.csv')
league_of_legends_df = pd.read_csv('archive/LeagueofLegends.csv')

# Tabs para organizar el contenido
tab_descripcion, tab_frecuencia_campeones, tab_bans, tab_comparativo = st.tabs([
    "Descripción", "Frecuencia de Campeones por Rol", "Frecuencia de Bans", "Análisis Comparativo"])

#----------------------------------------------------------
# Descripción
#----------------------------------------------------------
with tab_descripcion:
    st.markdown('''
    ## Análisis Avanzado de Composición de Campeones y Estrategias de Ban en League of Legends

    Este análisis presenta:
    - Frecuencia de selección de campeones en cada rol.
    - Estrategias de ban y su impacto potencial en el juego.
    - Comparación de campeones seleccionados entre equipos.
    ''')

#----------------------------------------------------------
# Frecuencia de Campeones por Rol
#----------------------------------------------------------
with tab_frecuencia_campeones:
    st.header("Frecuencia de Selección de Campeones por Rol")

    roles = {
        "Top": ("blueTopChamp", "redTopChamp"),
        "Jungle": ("blueJungleChamp", "redJungleChamp"),
        "Middle": ("blueMiddleChamp", "redMiddleChamp"),
        "ADC": ("blueADCChamp", "redADCChamp"),
        "Support": ("blueSupportChamp", "redSupportChamp")
    }

    role_frequencies = {role: {} for role in roles}

    # Calcular frecuencias
    for role, (blue_role_col, red_role_col) in roles.items():
        for champ in match_info_df[blue_role_col].dropna():
            role_frequencies[role][champ] = role_frequencies[role].get(champ, 0) + 1
        for champ in match_info_df[red_role_col].dropna():
            role_frequencies[role][champ] = role_frequencies[role].get(champ, 0) + 1

    # Convertir a DataFrame
    role_frequencies_df = pd.DataFrame.from_dict(role_frequencies, orient='index').fillna(0).astype(int)

    # Visualización por rol con gráficos avanzados
    for role in roles:
        role_data = role_frequencies_df.loc[role].sort_values(ascending=False).head(10)
        fig = px.bar(role_data, x=role_data.index, y=role_data.values,
                     labels={'x': f'Campeones en {role}', 'y': 'Frecuencia'},
                     title=f"Top 10 Campeones en el Rol de {role}",
                     color=role_data.values, color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------
# Frecuencia de Bans
#----------------------------------------------------------
with tab_bans:
    st.header("Análisis de Frecuencia de Bans")

    # Conteo de bans
    ban_frequencies = {}
    for bans in league_of_legends_df['redBans'].dropna():
        bans = eval(bans)
        for champ in bans:
            ban_frequencies[champ] = ban_frequencies.get(champ, 0) + 1

    ban_frequencies_df = pd.DataFrame(list(ban_frequencies.items()), columns=['Champion', 'Ban_Frequency']).sort_values(by='Ban_Frequency', ascending=False)

    # Gráfico de Bans
    fig_bans = px.bar(ban_frequencies_df.head(10), x='Champion', y='Ban_Frequency', 
                      title="Top 10 Campeones Más Baneados",
                      labels={'Champion': 'Campeón', 'Ban_Frequency': 'Frecuencia de Bans'},
                      color='Ban_Frequency', color_continuous_scale="reds")
    st.plotly_chart(fig_bans, use_container_width=True)

#----------------------------------------------------------
# Análisis Comparativo
#----------------------------------------------------------
with tab_comparativo:
    st.header("Análisis Comparativo entre Equipos (Azul vs Rojo)")

    # Frecuencia de selección por equipo
    team_data = {
        'Equipo': ['Azul', 'Rojo'],
        'Top': [match_info_df['blueTopChamp'].value_counts().idxmax(), match_info_df['redTopChamp'].value_counts().idxmax()],
        'Jungle': [match_info_df['blueJungleChamp'].value_counts().idxmax(), match_info_df['redJungleChamp'].value_counts().idxmax()],
        'Middle': [match_info_df['blueMiddleChamp'].value_counts().idxmax(), match_info_df['redMiddleChamp'].value_counts().idxmax()],
        'ADC': [match_info_df['blueADCChamp'].value_counts().idxmax(), match_info_df['redADCChamp'].value_counts().idxmax()],
        'Support': [match_info_df['blueSupportChamp'].value_counts().idxmax(), match_info_df['redSupportChamp'].value_counts().idxmax()]
    }
    team_comparison_df = pd.DataFrame(team_data)

    # Mostrar la comparación
    st.write("Comparativa de campeones más seleccionados entre equipos:")
    st.dataframe(team_comparison_df)

    # Gráfico de comparativa
    fig_compare = go.Figure(data=[
        go.Bar(name='Equipo Azul', x=team_comparison_df.columns[1:], y=team_comparison_df.loc[0, team_comparison_df.columns[1:]]),
        go.Bar(name='Equipo Rojo', x=team_comparison_df.columns[1:], y=team_comparison_df.loc[1, team_comparison_df.columns[1:]])
    ])
    fig_compare.update_layout(barmode='group', title="Comparativa de Campeones Más Seleccionados por Rol en Equipos Azul y Rojo")
    st.plotly_chart(fig_compare, use_container_width=True)
