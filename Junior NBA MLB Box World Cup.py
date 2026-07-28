import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la página web
st.set_page_config(
    page_title="JUNIOR - NBA Analytics", 
    page_icon="🏀", 
    layout="wide"
)

st.title("🏀 JUNIOR - SIMULADOR ANALÍTICO DE LA NBA")
st.write("Predicción avanzada de partidos de baloncesto basada en la Distribución Normal y Simulaciones de Montecarlo.")
st.write("---")

# 2. Base de datos integrada de equipos élite de la NBA
nba_teams = {
    "Boston Celtics": {"ppg_attack": 120.5, "ppg_defense": 109.2, "stdev": 10.4},
    "Oklahoma City Thunder": {"ppg_attack": 120.1, "ppg_defense": 111.0, "stdev": 11.2},
    "Denver Nuggets": {"ppg_attack": 114.9, "ppg_defense": 109.6, "stdev": 9.8},
    "Dallas Mavericks": {"ppg_attack": 117.9, "ppg_defense": 115.6, "stdev": 12.1},
    "Minnesota Timberwolves": {"ppg_attack": 113.0, "ppg_defense": 106.5, "stdev": 9.5}
}

# 3. Componentes visuales para elegir el partido
col1, col2, col3 = st.columns(3)
with col1: 
    local_b = st.selectbox("Equipo Local (Home)", list(nba_teams.keys()), index=0)
with col2: 
    vis_b = st.selectbox("Equipo Visitante (Away)", list(nba_teams.keys()), index=1)
with col3: 
    sims_b = st.slider("Simulaciones Montecarlo", 1000, 20000, 10000, 1000)

# 4. Botón ejecutor y motor matemático
if st.button("🔮 Simular Partido NBA Now"):
    if local_b == vis_b: 
        st.error("Un equipo no puede enfrentarse a sí mismo. Elige rivales diferentes.")
    else:
        with st.spinner("Corriendo 10,000 duelos virtuales en la duela..."):
            league_avg = 115.0
            
            # Proyección cruzada sumando la ventaja estadística de jugar en casa (+3 puntos)
            exp_home = nba_teams[local_b]["ppg_attack"] * (nba_teams[vis_b]["ppg_defense"] / league_avg) + 3.0
            exp_away = nba_teams[vis_b]["ppg_attack"] * (nba_teams[local_b]["ppg_defense"] / league_avg)

            home_wins, away_wins = 0, 0
            home_scores, away_scores = [], []

            # Bucle de simulación masiva
            for _ in range(sims_b):
                score_h = int(np.random.normal(exp_home, nba_teams[local_b]["stdev"]))
                score_v = int(np.random.normal(exp_away, nba_teams[vis_b]["stdev"]))
                
                # Resolución estricta de tiempos extras (Sin empates en la NBA)
                while score_h == score_v:
                    score_h += np.random.randint(5, 15)
                    score_v += np.random.randint(5, 15)
                
                home_scores.append(score_h)
                away_scores.append(score_v)
                
                if score_h > score_v: 
                    home_wins += 1
                else: 
                    away_wins += 1

            # Formatear porcentajes de victoria
            prob_home = round((home_wins / sims_b) * 100, 2)
            prob_away = round((away_wins / sims_b) * 100, 2)
            
            # Despliegue de resultados visuales
            st.success("¡Análisis estadístico de simulación completado!")
            st.write("---")
            
            m1, m2 = st.columns(2)
            m1.metric(f"Victoria {local_b}", f"{prob_home}%", f"Marcador Proyectado: {int(np.mean(home_scores))} pts")
            m2.metric(f"Victoria {vis_b}", f"{prob_away}%", f"Marcador Proyectado: {int(np.mean(away_scores))} pts")
            
            # Gráfico de densidad (Campana de Gauss interactiva)
            st.write("---")
            st.subheader("📊 Densidad de Puntuación y Frecuencia de Victoria")
            df_hist = pd.DataFrame({local_b: home_scores, vis_b: away_scores})
            fig = px.histogram(
                df_hist, 
                barmode='overlay', 
                title="Distribución de Puntos Obtenidos en las Simulaciones",
                labels={"value": "Puntos Totales", "variable": "Equipos"}
            )
            
            # TRUCO DE CORRECCIÓN: En Plotly 6.x la opacidad se aplica en los traces, no en el layout
            fig.update_traces(opacity=0.7)
            
            # Pintamos la gráfica en la pantalla web
            st.plotly_chart(fig, use_container_width=True)

