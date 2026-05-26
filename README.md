## Project Overview

AutoTest Recorder is a modern AI-powered Record & Playback Automation Platform that records real browser interactions and automatically generates clean, executable Playwright test scripts.

The platform is designed as a production-grade SaaS application with a modern responsive UI, smart selector generation, popup handling, playback execution, live logs, and exportable automation scripts.

It helps developers and QA teams create reliable browser automation without manually writing complex test code.

Key capabilities include:

* Browser interaction recording
* Intelligent Playwright code generation
* Playback execution engine
* Smart selector healing
* JavaScript dialog handling
* Real-time logs and diagnostics
* Screenshot capture on failure
* Modern glassmorphism-based UI

The system focuses on:

* Reliability
* Maintainability
* Automation accuracy
* Fault tolerance
* Smooth user experience
* Production-ready architecture
---
## Project Structure
```
/golden-response
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
```

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

This creates the full project under `./golden-response/`.

### Install and Start

```bash
cd golden-response

# Install all dependencies and Playwright browser
npm run setup

# Start frontend + backend in dev mode
npm run dev
```

Frontend runs at `http://localhost:3000`  
Backend API runs at `http://localhost:5000`
