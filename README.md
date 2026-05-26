## Project Overview

This repository contains all artifacts for a structured LLM evaluation exercise. A complex, domain-specific coding prompt was submitted to two large language models (ChatGPT / Response A and Gemini / Response B). Their outputs were analyzed across seven RLHF dimensions, and a golden reference implementation was produced.

The prompt asks for a **production-grade AI-powered Record & Playback Automation Tool** — a full-stack SaaS application that records browser interactions and generates executable Playwright test scripts.

---
## Project Structure
/autotest-recorder-golden-main
│
├── package.json
├── package-lock.json
├── README.md
├── render.yaml
│
├── frontend
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src
│       ├── main.jsx
│       ├── App.jsx
│       ├── components
│       │   ├── RecorderPanel.jsx
│       │   ├── PlaybackPanel.jsx
│       │   ├── StepEditor.jsx
│       │   ├── GeneratedCode.jsx
│       │   └── UrlInput.jsx
│       ├── pages
│       │   └── Dashboard.jsx
│       ├── hooks
│       │   └── useRecorder.js
│       ├── services
│       │   └── api.js
│       ├── store
│       │   └── recorderStore.js
│       └── styles
│           └── globals.css
│
├── backend
│   ├── package.json
│   └── src
│       ├── server.js
│       ├── routes
│       │   ├── recorder.routes.js
│       │   ├── playback.routes.js
│       │   └── generator.routes.js
│       ├── controllers
│       │   ├── recorder.controller.js
│       │   ├── playback.controller.js
│       │   └── generator.controller.js
│       ├── services
│       │   ├── recorder.service.js
│       │   ├── playback.service.js
│       │   └── generator.service.js
│       └── utils
│           └── logger.js
│
├── recorder
│   ├── browserRecorder.js
│   ├── selectorEngine.js
│   ├── eventListeners.js
│   └── highlightOverlay.js
│
├── generator
│   ├── playwrightGenerator.js
│   ├── stepFormatter.js
│   └── assertionGenerator.js
│
└── playback
    ├── playbackRunner.js
    ├── actionExecutor.js
    └── retryHandler.js

## Running 

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
