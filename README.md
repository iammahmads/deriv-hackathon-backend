# 🛡️ Sentinel | AI-Powered Risk Orchestration Dashboard

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![Cloudflare](https://img.shields.io/badge/Cloudflare_Pages-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://pages.cloudflare.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)

Sentinel is the visual command center for a multi-layered real-time risk orchestration system. Engineered for high-stakes financial environments (like the Deriv ecosystem), this dashboard transforms complex forensic data into actionable business intelligence at the Edge.

---

## 🔗 Repository Links

| Project | Repository Link |
| :--- | :--- |
| **Frontend** | [View GitHub](https://github.com/iammahmads/deriv-hackathon-frontend) |
| **Backend** | [View GitHub](https://github.com/iammahmads/deriv-hackathon-backend) |

---

## 🚀 Key Features

-   **📡 Real-Time Monitoring**
    Live-streaming feed of incoming transactions with instantaneous risk scoring and severity mapping.
-   **🧠 Forensic AI Insights**
    Large Language Model (LLM) generated "Verdicts" that provide human-readable explanations for every flagged transaction.
-   **🛡️ Triple-Engine Analysis**
    -   **Behavioral Engine:** Advanced velocity and smurfing detection.
    -   **Statistical Engine:** ML-driven (Random Forest) fraud probability scoring.
    -   **Structural Engine:** Graph-based analysis for money laundering and circular path detection.
-   **⚡ Edge Performance**
    Built on Next.js 16 and optimized for Cloudflare's Edge Runtime to ensure minimal latency for global risk monitoring.

---

## 🛠️ Tech Stack

-   **Framework:** [Next.js 16](https://nextjs.org/) (App Router)
-   **Styling:** [Tailwind CSS 4.0](https://tailwindcss.com/) + UI Components
-   **State & Data:** Supabase (Real-time DB) / REST API
-   **Deployment:** [Cloudflare Pages](https://pages.cloudflare.com/) via `@opennextjs/cloudflare`

---

## 🏗️ Getting Started

### Prerequisites

You'll need to define the following environment variables in a `.env.local` file:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

### Installation

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/iammahmads/deriv-hackathon-frontend.git
    cd deriv-hackathon-frontend
    ```

2.  **Install Dependencies**
    ```bash
    npm install
    ```

3.  **Run Locally**
    ```bash
    npm run dev
    ```

---

## 🌐 Deployment

This project is tailored for **Cloudflare Pages**.

1.  **Build Workflow**
    ```bash
    npx @cloudflare/next-on-pages
    ```

2.  **Deploy Command**
    ```bash
    npx wrangler pages deploy .vercel/output
    ```

---

## 🛡️ Sentinel Logic: The Hybrid Decision Engine

Every transaction surfaced in this dashboard is the result of a rigorous multi-stage verification pipeline:

1.  **Velocity Check:** Identifies rapid-fire transaction patterns.
2.  **ML Scoring:** 7-dimensional feature analysis via Random Forest.
3.  **Graph Monitoring:** Detects structural shifts and laundering cycles.
4.  **Forensic AI:** Synthesizes technical data into a concise textual verdict.

---

Developed for the **Deriv Hackathon** 🚀