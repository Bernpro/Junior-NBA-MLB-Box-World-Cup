# 🏆 JUNIOR - Multi-Sport Predictive Analytics Portal

An advanced sports data intelligence web application and simulation engine built with **Python** and **Streamlit**. This platform centralizes multiple mathematical modeling frameworks to simulate professional sports matches and calculate outcome probabilities for **Soccer (FIFA World Cup), Basketball (NBA), Baseball (MLB), and Professional Boxing**.

## 🚀 Analytical Capabilities by Sport

* **⚽ FIFA World Cup (Soccer):** Implements a **Poisson Distribution Engine** to compute independent joint probabilities for exact scorelines, combined with a **Monte Carlo Tournament Simulator** (10,000 runs) to track championship odds.
* **🏀 NBA Basketball (High-Scoring):** Utilizes a **Normal (Gaussian) Distribution Model** to project total points per game based on historical offensive/defensive margins and team consistency (Standard Deviation). Includes an automatic *Overtime (OT) Loop* simulator.
* **⚾ MLB Baseball (Sabermetrics):** Employs a specialized **Pitcher-vs-Batter Poisson Framework** that crosses team runs-scored metrics against the starting pitcher's Earned Run Average (ERA). Features automated *Extra Innings* resolution logic.
* **🥊 Professional Boxing (Event Probability):** Uses multi-variable randomized event loops to compute fight night performances based on historical win ratios, power landing metrics (KO%), and defensive ratings to project exact methods of victory (KO/TKO, Decision, or Draw).

## 🛠️ Technology Stack & Mathematical Framework
* **Interface & Web UI:** [Streamlit](https://streamlit.io)
* **Statistical Engines:** `scipy.stats.poisson` & `numpy.random.normal`
* **Data Scaffolding:** Pandas & NumPy
* **Interactive Visualizations:** [Plotly Express](https://plotly.com) (Responsive distribution curves, vertical/horizontal frequency histograms).

## 📦 Requirements & Installation
To clone this predictive dashboard and execute the statistical engines locally on your computer:
```bash
# Clone this repository
git clone https://github.com

# Navigate into the project directory
cd predictor-mundial

# Install the verified analytical dependencies
pip install -r requirements.txt

# Run the local instance of the application
streamlit run app.py
```

## ⚖️ Intellectual Property & License
This project is open-source and legally protected under the **GNU General Public License v3.0**. Commercial distribution or software derivations must comply with reciprocal open-source disclosure requirements.
