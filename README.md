# AI-Powered Coverage Analysis & Test Recommendation Engine

This project implements an **end-to-end AI-assisted coverage analysis pipeline** that helps verification engineers identify uncovered coverage gaps, understand why they exist, and generate **prioritized, actionable test suggestions**.

The system combines **deterministic coverage analysis** with **LLM-assisted reasoning (Gemini)** to improve coverage closure efficiency in complex hardware designs.

---

## 🚀 High-Level Architecture

```
Coverage Report (Text)
↓
[1] Parser
→ Structured Coverage JSON
↓
[2] Coverage Analyzer
→ Uncovered bins, cross gaps, impact analysis
↓
[3] LLM Agent (Gemini 2.5 Flash)
→ Test suggestions + reasoning
↓
[4] Prioritizer (Deterministic Scoring)
→ Sorted execution plan
↓
[5] Closure Predictor (Bonus)
→ Time estimates, probability, blockers
```

Each stage is **explicit, debuggable, and independently testable**.

---

## ✨ Key Features (Implemented)

- Functional coverage report parsing
- Detection of uncovered bins and cross-coverage gaps
- Pattern analysis (configuration gaps, concurrency gaps, error injection gaps)
- LLM-generated, engineering-realistic test suggestions
- **Graceful API error handling** (LLM failures never crash the pipeline)
- **Client-side rate limiting** for external LLM API usage
- **LLM response caching** for identical prompts
- Deterministic prioritization using assignment-defined formula
- Bonus: Coverage closure time and probability estimation

---

## 📁 Project Structure

```
dragonx-coverage-analyzer/
├── src/
│   ├── parser/          # Coverage report parsing
│   ├── analyzer/        # Pattern & impact analysis
│   ├── llm/             # Gemini LLM integration (safe, cached, rate-limited)
│   ├── prioritizer/     # Deterministic prioritization logic
│   ├── predictor/       # Coverage closure prediction (bonus)
│   └── main.py          # End-to-end pipeline runner
│
├── examples/
│   └── sample_report.txt
│
├── DESIGN.md            # Design & scalability discussion
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🛠 Setup Instructions

### 1️⃣ Prerequisites

- Python **3.9+**
- pip

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Gemini API Key Configuration

This project uses the modern Gemini API (google-genai) with the `gemini-2.5-flash` model.

For assignment/demo simplicity, the API key is hardcoded.

📍 **Edit the following file:**

```bash
src/llm/gemini_client.py
```

**Replace:**

```python
GEMINI_API_KEY = "PASTE_YOUR_API_KEY_HERE"
```

with your actual Gemini API key from Google AI Studio.

⚠️ **In a production system, this should be managed via environment variables or a secrets manager.**

---

## ▶️ How to Run

From the project root:

```bash
python3 src/main.py
```

---

## 🖥 What the Program Outputs

The pipeline prints all stages sequentially:

1. **Parsed Coverage Report**
   - Structured JSON representation of the input coverage report.

2. **Coverage Analysis Report**
   - Uncovered bins, cross-coverage gaps, detected patterns, and impact estimates.

3. **LLM Raw Test Suggestions**
   - Gemini-generated test ideas with reasoning, difficulty, and dependencies.

4. **Prioritized Test Plan**
   - Suggestions sorted using a deterministic scoring formula.

5. **Final Coverage Closure Plan**
   - Estimated effort, closure probability, and blockers (bonus feature).

Each stage is clearly labeled and printed as formatted JSON.

---

## 📊 Prioritization Logic

The prioritization strictly follows the assignment specification:

```diff
Priority Score =
  (Coverage Impact × 0.4)
+ (Inverse Difficulty × 0.3)
+ (Dependency Score × 0.3)
```

Where:

- **Coverage Impact** is computed analytically
- **Inverse Difficulty** = 1 / difficulty (easy=1, medium=2, hard=3)
- **Dependency Score** = 1 (no dependencies), 0.5 (dependencies exist)

This ensures deterministic, explainable prioritization.

---

## 📐 Design & Scalability

Detailed design discussions covering:

- 3+ dimensional cross coverage
- Learning from engineer feedback
- Scaling to designs with 100K+ coverage bins

are provided in `DESIGN.md`.

---

## ⚠️ Assumptions & Limitations

- Input coverage report format follows the provided sample structure
- Coverage impact estimation is heuristic-based
- LLM responses are non-deterministic by nature (mitigated via caching)
- Hardcoded API key is used only for assignment/demo purposes

---

## 🏁 Summary

This project demonstrates:

- Strong coverage analysis fundamentals
- Thoughtful and safe LLM integration
- Deterministic decision-making layered over AI
- Scalable system design aligned with real verification workflows

It is intentionally built to resemble a real AI-assisted verification productivity tool, not a standalone script.
