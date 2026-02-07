# 🛡️ Sentinel | AI-Powered Risk Orchestration Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.1-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Supabase](https://img.shields.io/badge/Supabase-2.27.3-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.8.0-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

Sentinel Backend is the core intelligence engine for a multi-layered real-time risk orchestration system. It processes incoming transactions through a hybrid pipeline of behavioral, statistical, and structural analysis, providing forensic insights at the scale of high-stakes financial environments.

---

## 🔗 Repository Links

| Project | Repository Link |
| :--- | :--- |
| **Frontend** | [View GitHub](https://github.com/iammahmads/deriv-hackathon-frontend) |
| **Backend** | [View GitHub](https://github.com/iammahmads/deriv-hackathon-backend) |

---

## 🚀 Key Features

- **📡 Triple-Engine Analysis**
    - **Behavioral Engine:** Velocity and "Smurfing" detection to identify rapid-fire transaction patterns.
    - **Statistical Engine:** ML-driven scoring (Random Forest/XGBoost) to calculate fraud probabilities based on high-dimensional features.
    - **Structural Engine:** Graph-based analysis (NetworkX) to detect money laundering cycles and circular paths.
- **🧠 Forensic AI Verdicts**
    Integrates with OpenAI to synthesize complex technical flags into human-readable forensic explanations.
- **🛡️ Real-Time Persistence**
    Seamlessly integrates with Supabase for real-time transaction logging and high-confidence alerting.
- **⚡ High Performance**
    Built with FastAPI for asynchronous transaction processing and sub-second risk orchestration.

---

## 🛠️ Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Machine Learning:** [Scikit-learn](https://scikit-learn.org/), [Pandas](https://pandas.pydata.org/), [XGBoost](https://xgboost.readthedocs.io/)
- **Graph Analysis:** [NetworkX](https://networkx.org/)
- **Forensic AI:** [OpenAI API](https://openai.com/blog/openai-api)
- **Database:** [Supabase](https://supabase.com/) (PostgreSQL + Real-time)

---

## 🏗️ Getting Started

### Prerequisites

- Python 3.10+
- A Supabase project
- An OpenAI API Key

### Environment Setup

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_or_service_role_key
BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
OPENAI_API_KEY=your_openai_api_key
```

### Installation

1. **Clone the Repo**
   ```bash
   git clone https://github.com/iammahmads/deriv-hackathon-backend.git
   cd deriv-hackathon-backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`. You can access the interactive documentation at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Testing with Simulator

You can use the built-in simulator to send mock transactions:
```bash
python -m app.services.simulator
```

---

## 📡 API Usage

### `POST /v1/analyze`

Analyzes a transaction for fraud and money laundering.

**Headers:**
- `X-OpenAI-Key`: Your OpenAI API Key (required for forensic AI).

**Payload:**
```json
{
  "tx_id": "TX-1234",
  "sender_id": "user_1",
  "receiver_id": "user_2",
  "amount": 500.0,
  "type": "TRANSFER",
  "features": [500.0, 1000.0, 500.0, 0.0, 500.0, 0.0, 0.0]
}
```

---

## 🛡️ Sentinel Logic: The Hybrid Decision Engine

Every transaction is passed through a four-stage verification pipeline:

1. **Velocity Check:** Monitors the rate of transactions for a specific sender to flag potential automation or smurfing.
2. **ML Scoring:** Analyzes a 7-dimensional feature vector using a pre-trained model to produce a statistical risk score.
3. **Graph Monitoring:** Maps transactions into a graph to identify structural anomalies like circular paths (laundering).
4. **Forensic AI:** If thresholds are met, the aggregated data is sent to an LLM to generate a plain-English "Forensic Verdict" for compliance officers.

---

Developed for the **Deriv Hackathon** 🚀