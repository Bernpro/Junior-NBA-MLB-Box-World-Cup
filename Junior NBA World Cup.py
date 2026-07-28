import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import plotly.express as px

# =====================================================================
# 1. CONFIGURACIÓN GENERAL DEL PORTAL DE JUNIOR
# =====================================================================
st.set_page_config(
    page_title="JUNIOR - Sports Analytics", 
    page_icon="🏆", 
    layout="wide"
)

st.title("🏆 JUNIOR - PORTAL DE ANALÍTICA DEPORTIVA")
st.write("Herramientas de simulación avanzada basadas en Ciencia de Datos y Modelos Estadísticos.")

# Barra selectora principal en la parte superior
deporte = st.selectbox("🎯 Elige el Deporte a Simular", ["⚽ Copa del Mundo (Fútbol)", "🏀 NBA Basketball"])

st.write("---")

# =====================================================================
# 2. SECCIÓN: COPA DEL MUNDO (FÚTBOL / POISSON)
# =====================================================================
if deporte == "⚽ Copa del Mundo (Fútbol)":
    st.subheader("⚽ Simulador Estadístico de la Copa del Mundo")
    st.write("Predicciones de partidos cortos utilizando la Distribución de Poisson y Montecarlo.")

    # Datos integrados de fútbol
    futbol_teams = {
        "Spain": {"attack": 2.1, "defense": 0.7},
        "England": {"attack": 2.0, "defense": 0.8},
        "Argentina": {"attack": 2.2, "defense": 0.7},
    }

    def calculate_exact_scores(home, away):
        exp_home = futbol_teams[home]["attack"] * futbol_teams[away]["defense"]
        exp_away = futbol_teams[away]["attack"] * futbol_teams[home]["defense"]
        score_matrix = []
        for h_g in range(5):
            for a_g in range(5):
                prob = poisson.pmf(h_g, exp_home) * poisson.pmf(a_g, exp_away) * 100
                score_matrix.append({
                    "Scoreline": f"{home} {h_g} - {a_g} {away}", 
                    "Probability (%)": round(prob, 2)
                })
        df_scores = pd.DataFrame(score_matrix)
        return df_scores.sort_values(by="Probability (%)", ascending=False).head(5)

    def simulate_futbol_match(home, away):
        exp_home = futbol_teams[home]["attack"] * futbol_teams[away]["defense"]
        exp_away = futbol_teams[away]["attack"] * futbol_teams[home]["defense"]
        h_g = np.random.poisson(exp_home)
        a_g = np.random.poisson(exp_away)
        if h_g > a_g: return home
        elif a_g > h_g: return away
        else: return np.random.choice([home, away])

    # Interfaz Web Fútbol
    col1, col2, col3 = st.columns(3)
    with col1:
        local_f = st.selectbox("Selecciona Equipo Local", list(futbol_teams.keys()), index=1)
    with col2:
        vis_f = st.selectbox("Selecciona Equipo Visitante", list(futbol_teams.keys()), index=2)
    with col3:
        sims_f = st.slider("Simulaciones Montecarlo (Fútbol)", 1000, 20000, 10000, 1000)

    if st.button("🔮 Calcular Predicción Fútbol"):
        if local_f == vis_f:
            st.error("Un equipo no puede jugar contra sí mismo.")
        else:
            with st.spinner("Corriendo motores de Poisson..."):
                df_top_scores = calculate_exact_scores(local_f, vis_f)
                
                # Bucle Montecarlo Torneo
                trophy_cabinet = {}
                for _ in range(sims_f):
                    semi_winner = simulate_futbol_match(local_f, vis_f)
                    champion = simulate_futbol_match("Spain", semi_winner)
                    trophy_cabinet[champion] = trophy_cabinet.get(champion, 0) + 1

                df_bracket = pd.DataFrame.from_dict(trophy_cabinet, orient="index", columns=["Wins"])
                df_bracket["Win Probability (%)"] = round((df_bracket["Wins"] / sims_f) * 100, 2)
                df_bracket = df_bracket.sort_values(by="Wins", ascending=False).reset_index().rename(columns={"index": "Country"})

                # Gráficos
                w_col1, w_col2 = st.columns(2)
                with w_col1:
                    st.subheader(f"📊 Top 5 Marcadores Probables")
                    fig1 = px.bar(df_top_scores, x="Probability (%)", y="Scoreline", orientation='h', text="Probability (%)", color="Probability (%)", color_continuous_scale="Blues")
                    fig1.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig1, use_container_width=True)
                with w_col2:
                    st.subheader("🏆 Probabilidades de Alzar el Título")
                    fig2 = px.bar(df_bracket, x="Country", y="Win Probability (%)", text="Win Probability (%)", color="Country", color_discrete_map={"Spain": "gold", "England": "tomato", "Argentina": "lightgreen"})
                    st.plotly_chart(fig2, use_container_width=True)

# =====================================================================
# 3. SECCIÓN: NBA BASKETBALL (DISTRIBUCIÓN NORMAL / GAUSSIANA)
# =====================================================================
elif deporte == "🏀 NBA Basketball":
    st.subheader("🏀 Simulador Analítico de la NBA")
    st.write("Predicción de partidos de alto puntaje basada en Distribución Normal y Simulaciones de Montecarlo.")

    nba_teams = {
        "Boston Celtics": {"ppg_attack": 120.5, "ppg_defense": 109.2, "stdev": 10.4},
        "Oklahoma City Thunder": {"ppg_attack": 120.1, "ppg_defense": 111.0, "stdev": 11.2},
        "Denver Nuggets": {"ppg_attack": 114.9, "ppg_defense": 109.6, "stdev": 9.8},
        "Dallas Mavericks": {"ppg_attack": 117.9, "ppg_defense": 115.6, "stdev": 12.1},
        "Minnesota Timberwolves": {"ppg_attack": 113.0, "ppg_defense": 106.5, "stdev": 9.5}
    }

    # Interfaz Web NBA
    col1, col2, col3 = st.columns(3)
    with col1:
        local_b = st.selectbox("Equipo Local (Home)", list(nba_teams.keys()), index=0)
    with col2:
        vis_b = st.selectbox("Equipo Visitante (Away)", list(nba_teams.keys()), index=1)
    with col3:
        sims_b = st.slider("Simulaciones Montecarlo (NBA)", 1000, 20000, 10000, 1000)

    if st.button("🔮 Simular Partido NBA Now"):
        if local_b == vis_b:
            st.error("Un equipo no puede enfrentarse a sí mismo.")
        else:
            with st.spinner("Corriendo simulaciones en la duela..."):
                league_avg = 115.0
                exp_home = nba_teams[local_b]["ppg_attack"] * (nba_teams[vis_b]["ppg_defense"] / league_avg) + 3.0
                exp_away = nba_teams[vis_b]["ppg_attack"] * (nba_teams[local_b]["ppg_defense"] / league_avg)

                home_wins, away_wins = 0, 0
                home_scores, away_scores = [], []

                for _ in range(sims_b):
                    score_h = int(np.random.normal(exp_home, nba_teams[local_b]["stdev"]))
                    score_v = int(np.random.normal(exp_away, nba_teams[vis_b]["stdev"]))
                    
                    while score_h == score_v:
                        score_h += np.random.randint(5, 15)
                        score_v += np.random.randint(5, 15)
                    
                    home_scores.append(score_h)
                    away_scores.append(score_v)
                    if score_h > score_v: home_wins += 1
                    else: away_wins += 1

                prob_home = round((home_wins / sims_b) * 100, 2)
                prob_away = round((away_wins / sims_b) * 100, 2)
                
                # Despliegue de Resultados
                st.success("¡Análisis de duela completado!")
                m1, m2 = st.columns(2)
                m1.metric(f"Victoria {local_b}", f"{prob_home}%", f"Marcador Proyectado: {int(np.mean(home_scores))} pts")
                m2.metric(f"Victoria {vis_b}", f"{prob_away}%", f"Marcador Proyectado: {int(np.mean(away_scores))} pts")
                
                # Gráfico Gaussiano
                st.write("---")
                df_hist = pd.DataFrame({local_b: home_scores, vis_b: away_scores})
                fig = px.histogram(df_hist, barmode='overlay', title="Campana de Gauss: Puntuación Esperada", labels={"value": "Puntos", "variable": "Equipos"})
                fig.update_layout(opacity=0.7, xaxis_title="Puntos Totales", yaxis_title="Partidos Simulados")
                st.plotly_chart(fig, use_container_width=True)

                fig_box = px.bar(df_box, x="Método de Victoria", y="Probabilidad (%)", text="Probabilidad (%)", color="Método de Victoria", title="Análisis Detallado de Resultados en las Tarjetas/Ring")
                st.plotly_chart(fig_box, use_container_width=True)


