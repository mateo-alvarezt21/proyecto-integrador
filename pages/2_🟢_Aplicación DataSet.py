import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(layout="wide")

st.title("Análisis Avanzado en League of Legends")

# Cargar datasets
match_info_df = pd.read_csv('archive/matchinfo.csv')
league_of_legends_df = pd.read_csv('archive/LeagueofLegends.csv')
gold_df = pd.read_csv('archive/gold.csv')
kills_df = pd.read_csv('archive/kills.csv')
structures_df = pd.read_csv('archive/structures.csv')

# Tabs para organizar el contenido
tab_descripcion, tab_frecuencia_campeones, tab_bans, tab_comparativo, tab_ganadores, tab_gold, tab_kills, tab_structures = st.tabs([
    "Descripción", "Frecuencia de Campeones por Rol", "Frecuencia de Bans", "Análisis Comparativo", 
    "Análisis de Campeones Más Seleccionados", "Análisis de Oro", "Análisis de Muertes", "Análisis de Estructuras"])

#----------------------------------------------------------
# Descripción
#----------------------------------------------------------
with tab_descripcion:
    st.markdown('''
    ## Análisis Avanzado de Composición de Campeones y Estrategias en League of Legends

    Este análisis presenta:
    - Frecuencia de selección de campeones en cada rol.
    - Estrategias de ban y su impacto potencial en el juego.
    - Comparación de campeones seleccionados entre equipos.
    - Análisis de campeones más seleccionados.
    - Evolución de la diferencia de oro entre equipos a lo largo del tiempo.
    - Distribución y localización de muertes en el campo de batalla.
    - Destrucción de estructuras y su impacto en la partida.
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

    for role, (blue_role_col, red_role_col) in roles.items():
        for champ in match_info_df[blue_role_col].dropna():
            role_frequencies[role][champ] = role_frequencies[role].get(champ, 0) + 1
        for champ in match_info_df[red_role_col].dropna():
            role_frequencies[role][champ] = role_frequencies[role].get(champ, 0) + 1

    role_frequencies_df = pd.DataFrame.from_dict(role_frequencies, orient='index').fillna(0).astype(int)

    campeones_top_n = st.slider("Selecciona el número de campeones a mostrar", min_value=5, max_value=20, value=10)
    for role in roles:
        role_data = role_frequencies_df.loc[role].sort_values(ascending=False).head(campeones_top_n)
        fig = px.bar(role_data, x=role_data.index, y=role_data.values,
                     labels={'x': f'Campeones en {role}', 'y': 'Frecuencia'},
                     title=f"Top {campeones_top_n} Campeones en el Rol de {role}",
                     color=role_data.values, color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------
# Frecuencia de Bans
#----------------------------------------------------------
with tab_bans:
    st.header("Análisis de Frecuencia de Bans")

    ban_frequencies = {}
    for bans in league_of_legends_df['redBans'].dropna():
        bans = eval(bans)
        for champ in bans:
            ban_frequencies[champ] = ban_frequencies.get(champ, 0) + 1

    ban_frequencies_df = pd.DataFrame(list(ban_frequencies.items()), columns=['Champion', 'Ban_Frequency']).sort_values(by='Ban_Frequency', ascending=False)

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

    team_data = {
        'Equipo': ['Azul', 'Rojo'],
        'Top': [match_info_df['blueTopChamp'].value_counts().idxmax(), match_info_df['redTopChamp'].value_counts().idxmax()],
        'Jungle': [match_info_df['blueJungleChamp'].value_counts().idxmax(), match_info_df['redJungleChamp'].value_counts().idxmax()],
        'Middle': [match_info_df['blueMiddleChamp'].value_counts().idxmax(), match_info_df['redMiddleChamp'].value_counts().idxmax()],
        'ADC': [match_info_df['blueADCChamp'].value_counts().idxmax(), match_info_df['redADCChamp'].value_counts().idxmax()],
        'Support': [match_info_df['blueSupportChamp'].value_counts().idxmax(), match_info_df['redSupportChamp'].value_counts().idxmax()]
    }
    team_comparison_df = pd.DataFrame(team_data)

    st.write("Comparativa de campeones más seleccionados entre equipos:")
    st.dataframe(team_comparison_df)

    fig_compare = go.Figure(data=[
        go.Bar(name='Equipo Azul', x=team_comparison_df.columns[1:], y=team_comparison_df.loc[0, team_comparison_df.columns[1:]]),
        go.Bar(name='Equipo Rojo', x=team_comparison_df.columns[1:], y=team_comparison_df.loc[1, team_comparison_df.columns[1:]])
    ])
    fig_compare.update_layout(barmode='group', title="Comparativa de Campeones Más Seleccionados por Rol en Equipos Azul y Rojo")
    st.plotly_chart(fig_compare, use_container_width=True)

#----------------------------------------------------------
# Análisis de Oro
#----------------------------------------------------------
with tab_gold:
    st.header("Análisis de Diferencias de Oro a lo Largo del Tiempo")

    gold_diff_df = gold_df[gold_df['Type'] == 'golddiff']
    gold_diff_df = gold_diff_df.drop(columns=['Address', 'Type'])
    gold_diff_df = gold_diff_df.melt(var_name='Minute', value_name='Gold Difference')
    gold_diff_df['Minute'] = gold_diff_df['Minute'].str.extract(r'(\d+)').astype(int)
    fig_gold = px.line(gold_diff_df, x='Minute', y='Gold Difference', title="Evolución de la Diferencia de Oro",
                       labels={'Minute': 'Minuto', 'Gold Difference': 'Diferencia de Oro'},
                       color_discrete_sequence=["gold"])
    st.plotly_chart(fig_gold, use_container_width=True)

#----------------------------------------------------------
# Análisis de Muertes
#----------------------------------------------------------
with tab_kills:
    st.header("Análisis de Distribución de Muertes y Mapa de Calor")

    # Filtrar solo las filas con valores numéricos en 'x_pos' y 'y_pos'
    kills_df = kills_df[pd.to_numeric(kills_df['x_pos'], errors='coerce').notnull()]
    kills_df = kills_df[pd.to_numeric(kills_df['y_pos'], errors='coerce').notnull()]
    kills_df['x_pos'] = kills_df['x_pos'].astype(float)
    kills_df['y_pos'] = kills_df['y_pos'].astype(float)

    # Distribución de muertes a lo largo del tiempo
    fig_kills_time = px.histogram(
        kills_df, 
        x='Time', 
        color='Team', 
        nbins=50,
        title="Distribución de Muertes a lo Largo del Tiempo",
        labels={'Time': 'Tiempo (min)', 'count': 'Número de Muertes'}
    )
    st.plotly_chart(fig_kills_time, use_container_width=True)

    # Mapa de calor de muertes en el campo de batalla
    fig_kills_heatmap = px.density_heatmap(
        kills_df, 
        x='x_pos', 
        y='y_pos', 
        color_continuous_scale='Viridis',
        title="Mapa de Calor de Localización de Muertes",
        labels={'x_pos': 'Posición X', 'y_pos': 'Posición Y'}
    )

    # Ajustar las dimensiones para hacerlo cuadrado
    fig_kills_heatmap.update_layout(
        width=600,  # Ancho en píxeles
        height=600,  # Alto en píxeles
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        )
    )

    st.plotly_chart(fig_kills_heatmap, use_container_width=True)


#----------------------------------------------------------
# Análisis de Estructuras
#----------------------------------------------------------
with tab_structures:
    st.header("Análisis de Destrucción de Estructuras")

    # Conteo de estructuras destruidas por tipo y equipo
    structures_count_df = structures_df.groupby(['Team', 'Type']).size().reset_index(name='Count')

    # Gráfico de barras para estructuras destruidas por tipo y equipo
    fig_structures = px.bar(structures_count_df, x='Type', y='Count', color='Team', barmode='group',
                            title="Destrucción de Estructuras por Tipo y Equipo",
                            labels={'Type': 'Tipo de Estructura', 'Count': 'Número de Estructuras Destruidas'})
    st.plotly_chart(fig_structures, use_container_width=True)

    # Línea de tiempo de destrucción de estructuras
    structures_df['Time'] = structures_df['Time'].astype(float)
    fig_structures_timeline = px.scatter(structures_df, x='Time', y='Type', color='Team', 
                                         title="Línea de Tiempo de Destrucción de Estructuras",
                                         labels={'Time': 'Tiempo (min)', 'Type': 'Tipo de Estructura'},
                                         hover_data=['Lane'])
    fig_structures_timeline.update_traces(marker=dict(size=10, opacity=0.6))
    st.plotly_chart(fig_structures_timeline, use_container_width=True)

    # Distribución de destrucción por línea
    st.subheader("Distribución de Destrucción de Estructuras por Línea")
    lane_count_df = structures_df.groupby(['Lane', 'Type']).size().reset_index(name='Count')
    fig_lane_distribution = px.bar(lane_count_df, x='Lane', y='Count', color='Type', barmode='stack',
                                   title="Distribución de Estructuras Destruidas por Línea",
                                   labels={'Lane': 'Línea', 'Count': 'Número de Estructuras Destruidas'})
    st.plotly_chart(fig_lane_distribution, use_container_width=True)
