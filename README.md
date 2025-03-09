# 🏅 Olympics Analysis Dashboard

## ✨ Overview
The **Olympics Analysis Dashboard** is a Streamlit-based web application designed to provide insightful visualizations and trends from historical Olympic data. It allows users to explore key statistics, medal tallies, country-wise performances, and athlete trends interactively.

---
## 🔄 Features
- ✨ **Medal Tally:** View overall medal counts or filter by specific years and countries.
- ✨ **Overall Analysis:** Key statistics on Olympic editions, hosts, sports, events, nations, and athletes.
- ✨ **Country-Wise Analysis:** Trend analysis for individual countries with visualizations.
- ✨ **Athlete Analysis:** Insights into age distributions, height vs. weight comparisons, and gender trends.

---
## 🛀 Project Structure
```
.
├── app.py              # Main Streamlit application
├── helper.py           # Data processing and helper functions
├── preprocessor.py     # Data cleaning and preprocessing functions
├── dataset/            # Contains athlete_events.csv and noc_regions.csv
└── README.md           # Project documentation (this file)
```

---
## 📚 Getting Started

### ✅ 1. Clone the Repository
```bash
git clone https://your-repository-url.git
cd your-repository-directory
```

### ✅ 2. Create a Virtual Environment
Create a virtual environment to manage dependencies:
#### **Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
#### **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### ✅ 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### ✅ 4. Running the Application
```bash
streamlit run app.py
```
The app will be accessible at the displayed local URL.

---
## 🛠️ Git Workflow

### ⚙️ Staging, Committing, and Pushing Changes
```bash
git status   # Check current status
git add .    # Stage all changes
git commit -m "Your descriptive message"  # Commit with a message
git push origin main  # Push changes to the main branch
```

---
## 📊 Additional Notes
- **🔍 Data Preprocessing:** The app processes `athlete_events.csv` and `noc_regions.csv` using `preprocessor.py`.
- **🔧 Helper Functions:** Data transformation and visualization functions are in `helper.py`.
- **🎨 Visualizations:** Interactive charts are built using Plotly and Matplotlib in Streamlit.

Enjoy exploring Olympic history with this dynamic dashboard! 🏅🌟

