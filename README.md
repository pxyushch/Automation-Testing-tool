# AutoTest Recorder — LLM Evaluation

> **Domain:** DevOps / QA Automation / SaaS Engineering  
> **Prompt Author:** Piyush Chauhan  
> **Purpose:** Post-training RLHF assessment — evaluating LLM code generation quality

---

## Project Overview

This repository contains all artifacts for a structured LLM evaluation exercise. A complex, domain-specific coding prompt was submitted to two large language models (ChatGPT / Response A and Gemini / Response B). Their outputs were analyzed across seven RLHF dimensions, and a golden reference implementation was produced.

The prompt asks for a **production-grade AI-powered Record & Playback Automation Tool** — a full-stack SaaS application that records browser interactions and generates executable Playwright test scripts.

---

## Repository Structure

```
.
├── prompt.md              # Original domain-specific coding prompt
├── justification.md       # Side-by-side evaluation of Response A vs Response B
├── golden_response.py     # Executable Python script that generates the full project scaffold
└── README.md              # This file
```

---

## File Descriptions

### `prompt.md`
The original prompt given to both LLMs. It covers:
- A realistic industry task (QA automation / DevOps)
- 7 explicit, checkable constraints (tech stack, selector strategy, dialog handling, code quality, UI/UX, folder structure, setup commands)
- Technical and formatting requirements
- Complexity sufficient to meaningfully differentiate LLM responses

### `justification.md`
A structured evaluation framework comparing Response A (ChatGPT) and Response B (Gemini), including:
- 7-dimension RLHF scoring table
- Side-by-side strengths and weaknesses
- Deep analysis of architecture, Playwright correctness, selector compliance, and UI implementation
- Final verdict with reasoning

### `golden_response.py`
The ideal benchmark solution. Running this script generates the complete production-ready project:
- All frontend React components (RecorderPanel, PlaybackPanel, GeneratedCode, UrlInput)
- Full backend Express server with routes, controllers, services
- Recorder engine (browserRecorder, eventListeners, selectorEngine, dialogHandler)
- Playwright code generator with correct dialog-before-trigger ordering
- Playback engine with retry and screenshot-on-failure
- Shared constants, helpers, and logger
- Package.json files, Vite/Tailwind config, README, example `.spec.js`

---

## Running / Testing the Golden Response

### Prerequisites
- Python 3.8 or higher
- Node.js 18+ and npm

### Generate the Project Scaffold

```bash
# Run the golden response generator
python golden_response.py

# Or specify a custom output directory
python golden_response.py --output-dir ./my-autotest-recorder
```

This creates the full project under `./autotest-recorder-golden/`.

### Install and Start

```bash
cd autotest-recorder-golden

# Install all dependencies and Playwright browser
npm run setup

# Start frontend + backend in dev mode
npm run dev
```

Frontend runs at `http://localhost:3000`  
Backend API runs at `http://localhost:5000`

### Verify the Generated Code Quality

Open the app, set a target URL, click **Start Recording**, interact with the page, click **Stop**, then click **Generate**. The generated code should:
- Use `@playwright/test` with `async/await`
- Contain no `waitForTimeout()`
- Have dialog handlers registered **before** the triggering action
- Follow the 6-tier selector priority

---

## Evaluation Methodology

Responses were scored across **7 RLHF dimensions**:

| Dimension | What It Measures |
|-----------|-----------------|
| **Correctness** | Technical accuracy — valid code, correct Playwright patterns, proper async handling |
| **Relevance** | Alignment with every explicit constraint in the prompt |
| **Completeness** | Coverage of all required modules, outputs, and edge cases |
| **Style & Presentation** | Code formatting, naming conventions, readability |
| **Coherence** | Internal consistency — architecture, module boundaries, runtime safety |
| **Helpfulness** | Usability as a real engineering starting point; developer experience |
| **Creativity** | Novel solutions, above-average architectural thinking |

### Scoring Scale
Each dimension scored 1.0–5.0. Higher is better.  
Final verdict uses qualitative analysis — not just total points — to identify systemic vs. additive flaws.

### Key Evaluation Finding

> Response A (ChatGPT) scored higher despite having fewer total files, because it maintained correct runtime layer separation and produced implementable code. Response B (Gemini) listed more modules but contained a disqualifying architectural flaw: importing Node.js backend code into the browser-side frontend.

See `justification.md` for the full analysis.

---

## Constraints Verified in Golden Response

| Constraint | Status |
|------------|--------|
| React + Tailwind + Framer Motion frontend | ✅ |
| Node.js + Express backend | ✅ |
| Playwright automation engine | ✅ |
| 6-tier selector priority | ✅ |
| Dialog handler before trigger | ✅ |
| No `waitForTimeout()` | ✅ |
| Screenshot on failure | ✅ |
| Retry with exponential back-off | ✅ |
| Dark glassmorphism UI | ✅ |
| Monaco editor + download button | ✅ |
| `npm run setup/dev/start/build` scripts | ✅ |
| Complete folder structure | ✅ |

---

*Repository created as part of the Piyush Chauhan Post-Training Assessment.*
