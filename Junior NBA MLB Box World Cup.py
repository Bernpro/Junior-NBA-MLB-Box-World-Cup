






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

st.title("🏆 JUNIOR - PORTAL MULTIDEPORTIVO DE ANALÍTICA")
st.write("Simulaciones predictivas basadas en Modelos de Distribución de Poisson, Gauss y Probabilidades de Evento.")

# Barra selectora principal con los 4 deportes
deporte = st.selectbox(
    "🎯 Elige el Deporte a Simular", 
    ["⚽ Copa del Mundo (Fútbol)", "🏀 NBA Basketball", "⚾ MLB Baseball", "🥊 Boxeo Profesional"]
)

st.write("---")

# =====================================================================
# 2. SECCIÓN: COPA DEL MUNDO (FÚTBOL)
# =====================================================================
if deporte == "⚽ Copa del Mundo (Fútbol)":
    st.subheader("⚽ Simulador Estadístico de la Copa del Mundo")
    st.write("Predicciones basadas en la Distribución de Poisson y Montecarlo.")

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

    col1, col2, col3 = st.columns(3)
    with col1: local_f = st.selectbox("Selecciona Equipo Local", list(futbol_teams.keys()), index=1)
    with col2: vis_f = st.selectbox("Selecciona Equipo Visitante", list(futbol_teams.keys()), index=2)
    with col3: sims_f = st.slider("Simulaciones Montecarlo (Fútbol)", 1000, 20000, 10000, 1000)

    if st.button("🔮 Calcular Predicción Fútbol"):
        if local_f == vis_f: st.error("Elige rivales diferentes.")
        else:
            with st.spinner("Procesando datos..."):
                df_top_scores = calculate_exact_scores(local_f, vis_f)
                trophy_cabinet = {}
                for _ in range(sims_f):
                    semi_winner = simulate_futbol_match(local_f, vis_f)
                    champion = simulate_futbol_match("Spain", semi_winner)
                    trophy_cabinet[champion] = trophy_cabinet.get(champion, 0) + 1

                df_bracket = pd.DataFrame.from_dict(trophy_cabinet, orient="index", columns=["Wins"])
                df_bracket["Win Probability (%)"] = round((df_bracket["Wins"] / sims_f) * 100, 2)
                df_bracket = df_bracket.sort_values(by="Wins", ascending=False).reset_index().rename(columns={"index": "Country"})

                w_col1, w_col2 = st.columns(2)
                with w_col1:
                    st.subheader("📊 Top 5 Marcadores Probables")
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
    st.write("Predicción de partidos basada en Distribución Normal y Simulaciones de Montecarlo.")

    nba_teams = {
        "Boston Celtics": {"ppg_attack": 120.5, "ppg_defense": 109.2, "stdev": 10.4},
        "Oklahoma City Thunder": {"ppg_attack": 120.1, "ppg_defense": 111.0, "stdev": 11.2},
        "Denver Nuggets": {"ppg_attack": 114.9, "ppg_defense": 109.6, "stdev": 9.8},
        "Dallas Mavericks": {"ppg_attack": 117.9, "ppg_defense": 115.6, "stdev": 12.1},
    }

    col1, col2, col3 = st.columns(3)
    with col1: local_b = st.selectbox("Equipo Local (Home)", list(nba_teams.keys()), index=0)
    with col2: vis_b = st.selectbox("Equipo Visitante (Away)", list(nba_teams.keys()), index=1)
    with col3: sims_b = st.slider("Simulaciones Montecarlo (NBA)", 1000, 20000, 10000, 1000)

    if st.button("🔮 Simular Partido NBA Now"):
        if local_b == vis_b: st.error("Elige rivales diferentes.")
        else:
            with st.spinner("Simulando duelos en la duela..."):
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
                
                st.success("¡Análisis completado!")
                m1, m2 = st.columns(2)
                m1.metric(f"Victoria {local_b}", f"{prob_home}%", f"Marcador Proyectado: {int(np.mean(home_scores))} pts")
                m2.metric(f"Victoria {vis_b}", f"{prob_away}%", f"Marcador Proyectado: {int(np.mean(away_scores))} pts")
                
                df_hist = pd.DataFrame({local_b: home_scores, vis_b: away_scores})
                fig = px.histogram(df_hist, barmode='overlay', title="Campana de Gauss: Puntuación Esperada", labels={"value": "Puntos", "variable": "Equipos"})
                st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 4. SECCIÓN: MLB BASEBALL (POISSON SIN EMPATES + PITCHERS)
# =====================================================================
elif deporte == "⚾ MLB Baseball":
    st.subheader("⚾ Simulador de Béisbol Sabermétrico de la MLB")
    st.write("Modelo de carreras estimadas cruzando el poder de bateo del equipo y la efectividad (ERA) del Pitcher abridor.")

    mlb_teams = {
        "LA Dodgers": {"runs_scored": 5.2, "pitcher_era": 3.40},
        "NY Yankees": {"runs_scored": 5.0, "pitcher_era": 3.65},
        "Houston Astros": {"runs_scored": 4.7, "pitcher_era": 3.80},
        "Atlanta Braves": {"runs_scored": 4.8, "pitcher_era": 3.45}
    }

    col1, col2, col3 = st.columns(3)
    with col1: local_m = st.selectbox("Equipo Local (Bateo)", list(mlb_teams.keys()), index=0)
    with col2: vis_m = st.selectbox("Equipo Visitante (Bateo)", list(mlb_teams.keys()), index=1)
    with col3: sims_m = st.slider("Simulaciones Montecarlo (MLB)", 1000, 20000, 10000, 1000)

    
	
	
	
	
	
	    if st.button("🔮 Simular Partido MLB"):
        if local_m == vis_m:
            st.error("Elige rivales diferentes.")
        else:
            with st.spinner("Lanzando simulaciones de entradas..."):
                league_era_avg = 4.00
                exp_home = mlb_teams[local_m]["runs_scored"] * (mlb_teams[vis_m]["pitcher_era"] / league_era_avg) + 0.2
                exp_away = mlb_teams[vis_m]["runs_scored"] * (mlb_teams[local_m]["pitcher_era"] / league_era_avg)

                home_wins, away_wins = 0, 0
                runs_h_list, runs_v_list = [], []

                for _ in range(sims_m):
                    runs_h = np.random.poisson(exp_home)
                    runs_v = np.random.poisson(exp_away)
                    
                    while runs_h == runs_v:
                        runs_h += np.random.choice([0, 1], p=[0.5, 0.5])
                        runs_v += np.random.choice([0, 1], p=[0.5, 0.5])
                    
                    runs_h_list.append(runs_h)
                    runs_v_list.append(runs_v)
                    
                    if runs_h > runs_v: 
                        home_wins += 1
                    else: 
                        away_wins += 1

                p_home = round((home_wins / sims_m) * 100, 2)
                p_away = round((away_wins / sims_m) * 100, 2)

                st.success("¡Simulación de Extra Innings completada!")
                c1, c2 = st.columns(2)
                c1.metric(f"Victoria {local_m}", f"{p_home}%", f"Carreras Proyectadas: {round(np.mean(runs_h_list), 1)}")
                c2.metric(f"Victoria {vis_m}", f"{p_away}%", f"Carreras Proyectadas: {round(np.mean(runs_v_list), 1)}")

                df_mlb_plot = pd.DataFrame({local_m: runs_h_list, vis_m: runs_v_list})
                fig_mlb = px.histogram(df_mlb_plot, barmode='group', title="Probabilidad de Carreras Anotadas por Partido", labels={"value": "Carreras"})
                st.plotly_chart(fig_mlb, use_container_width=True)

# =====================================================================
# 5. SECCIÓN: BOXEO (PROBABILIDADES DE EVENTO)
# =====================================================================
elif deporte == "🥊 Boxeo Profesional":
    st.subheader("🥊 Simulador de Combates de Boxeo")
    st.write("Análisis probabilístico basado en el registro de peleas, poder de pegada (KO%) y resistencia de los peleadores.")

    fighters = {
        "Canelo Álvarez": {"win_ratio": 0.88, "ko_ratio": 0.65, "defense": 0.90},
        "David Benavidez": {"win_ratio": 0.95, "ko_ratio": 0.85, "defense": 0.80},
        "Dmitry Bivol": {"win_ratio": 0.92, "ko_ratio": 0.52, "defense": 0.95},
        "Artur Beterbiev": {"win_ratio": 1.00, "ko_ratio": 1.00, "defense": 0.78}
    }

    col1, col2, col3 = st.columns(3)
    with col1: 
        box_1 = st.selectbox("Boxeador Esquina Azul", list(fighters.keys()), index=0)
    with col2: 
        box_2 = st.selectbox("Boxeador Esquina Roja", list(fighters.keys()), index=1)
    with col3: 
        sims_box = st.slider("Simulaciones de Combate (Rondas)", 1000, 20000, 10000, 1000)

    if st.button("🥊 Iniciar Combate Estelar"):
        if box_1 == box_2: 
            st.error("Un boxeador no puede pelear contra sí mismo.")
        else:
            with st.spinner("Simulando los 12 asaltos en el ring..."):
                b1_wins_ko, b1_wins_dec = 0, 0
                b2_wins_ko, b2_wins_dec = 0, 0
                draws = 0

                for _ in range(sims_box):
                    perf_1 = fighters[box_1]["win_ratio"] * np.random.uniform(0.8, 1.2)
                    perf_2 = fighters[box_2]["win_ratio"] * np.random.uniform(0.8, 1.2)

                    if abs(perf_1 - perf_2) < 0.05:
                        draws += 1 
                    elif perf_1 > perf_2:
                        if np.random.uniform(0, 1) < (fighters[box_1]["ko_ratio"] * (1 - fighters[box_2]["defense"])):
                            b1_wins_ko += 1
                        else:
                            b1_wins_dec += 1
                    else:
                        if np.random.uniform(0, 1) < (fighters[box_2]["ko_ratio"] * (1 - fighters[box_1]["defense"])):
                            b2_wins_ko += 1
                        else:
                            b2_wins_dec += 1

                metodos = [
                    f"{box_1} por KO", f"{box_1} por Decisión", 
                    "Empate", 
                    f"{box_2} por Decisión", f"{box_2} por KO"
                ]
                conteos = [b1_wins_ko, b1_wins_dec, draws, b2_wins_dec, b2_wins_ko]
                porcentajes = [round((c / sims_box) * 100, 2) for c in conteos]

                df_box = pd.DataFrame({"Método de Victoria": metodos, "Probabilidad (%)": porcentajes})

                st.success("¡Campanazo final! Combate simulado.")
                
                total_b1 = round(porcentajes[0] + porcentajes[1], 2)
                total_b2 = round(porcentajes[3] + porcentajes[4], 2)
                
                bc1, bc2, bc3 = st.columns(3)
                bc1.metric(f"Victoria Total {box_1}", f"{total_b1}%")
                bc2.metric("Probabilidad de Empate", f"{porcentajes[2]}%")
                bc3.metric(f"Victoria Total {box_2}", f"{total_b2}%")

                st.write("---")
                fig_box = px.bar(df_box, x="Método de Victoria", y="Probabilidad (%)", text="Probabilidad (%)", color="Método de Victoria", title="Análisis Detallado de Resultados en las Tarjetas/Ring")
                st.plotly_chart(fig_box, use_container_width=True)


