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
tab_descripcion, tab_frecuencia_campeones, tab_kills, tab_structures = st.tabs([
    "Descripción", "Frecuencia de Campeones por Rol", 
    "Análisis de Muertes", "Análisis de Estructuras"])

#----------------------------------------------------------
# Descripción
#----------------------------------------------------------
with tab_descripcion:
    st.markdown('''
    ## League of Legends (LoL)

    League of Legends es un juego de estrategia en tiempo real y combate en equipo, desarrollado por Riot Games. 
    En el juego, los jugadores asumen el rol de "campeones" con habilidades únicas y trabajan en conjunto para 
    destruir la base del equipo contrario. Cada equipo está compuesto por cinco jugadores que ocupan roles específicos 
    en el mapa y seleccionan campeones estratégicamente para obtener ventaja.

    El juego se desarrolla en un mapa llamado *La Grieta del Invocador*, dividido en tres carriles (top, mid y bot) y 
    una jungla. El objetivo final es destruir el "Nexo" del equipo enemigo, protegido por torretas y otras estructuras. 
    Los equipos ganan oro a medida que eliminan súbditos, estructuras y campeones enemigos, lo que les permite 
    comprar objetos y mejorar sus estadísticas.

    ### Aspectos Clave del Análisis
    ''')
    
    # Imagen general de League of Legends (Mapa)
    st.image("https://e00-especiales-marca.uecdn.es/esports/images/worlds22/asi-se-juega/mapa.jpg", caption="Mapa de La Grieta del Invocador en League of Legends")

    st.markdown('''
    - *Frecuencia de Selección de Campeones por Rol*: En cada partida, los equipos seleccionan campeones que se ajusten a roles específicos 
      (Top, Jungle, Mid, ADC y Support). Aquí analizamos la popularidad de campeones en cada rol.

    - *Estrategias de Ban*: Los equipos pueden "banear" campeones para evitar que el equipo contrario los seleccione. Este análisis examina los campeones más baneados y el impacto de estas decisiones.

    - *Comparación de Campeones Seleccionados entre Equipos*: Comparación de los campeones elegidos por ambos equipos para evaluar cómo sus composiciones afectan los resultados de las partidas.

    - *Análisis de Campeones Más Seleccionados*: Un análisis detallado de los campeones más elegidos en diferentes roles y el impacto de su selección en las partidas.

    - *Evolución de la Diferencia de Oro*: Analizamos cómo varía la diferencia de oro entre los equipos a lo largo del tiempo, lo que indica la ventaja en términos de recursos.

    - *Distribución y Localización de Muertes*: Un mapa de calor que muestra las áreas del mapa donde ocurren más muertes, lo que permite observar patrones de pelea entre los equipos.

    - *Destrucción de Estructuras*: Análisis de las estructuras destruidas (como torretas e inhibidores) y su importancia en el progreso hacia la victoria.
    ''')

    # Imagen de los roles y carriles
    st.image("https://cloudfront-us-east-1.images.arcpublishing.com/infobae/NHUPXSKK45FQBA47AU6B7FDL6Q.png", caption="Roles y Carriles en League of Legends")


#----------------------------------------------------------
# Análisis Exploratorio
#----------------------------------------------------------
#with tab_exploratorio:
    # st.header("Análisis Exploratorio de Datos")

    # # Selector de Dataset
    # dataset_option = st.selectbox("Seleccione el Dataset para el Análisis Exploratorio", 
    #                               ("matchinfo", "LeagueofLegends", "gold", "kills", "structures"))

    # # Selección del DataFrame correspondiente
    # if dataset_option == "matchinfo":
    #     df = match_info_df
    # elif dataset_option == "LeagueofLegends":
    #     df = league_of_legends_df
    # elif dataset_option == "gold":
    #     df = gold_df
    # elif dataset_option == "kills":
    #     df = kills_df
    # elif dataset_option == "structures":
    #     df = structures_df

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
# with tab_bans:
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