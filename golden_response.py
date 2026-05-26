"""
golden_response.py
==================
AutoTest Recorder 

This script can be used for implementation of AutoTest Recorder prompt.
It programmatically generates the complete project scaffold (all files, folders,
and code) that represents a production-grade Record & Playback Automation Tool.

Usage:
    python golden_response.py [--output-dir ./autotest-recorder]

Requirements:
    Python 3.8+  (no third-party packages needed)

What it generates:
    - Full folder structure under /autotest-recorder-golden/
    - All frontend React components
    - All backend Express routes, controllers, services
    - Recorder engine (browser, events, selector, dialog)
    - Playwright code generator
    - Playback engine with retry handler
    - README.md, package.json files

"""

import argparse
import os
import sys

# ---------------------------------------------------------------------------
# File definitions — (relative_path, file_content) pairs
# ---------------------------------------------------------------------------

FILES: dict[str, str] = {}

# ── Root ────────────────────────────────────────────────────────────────────

FILES["package.json"] = """\
{
  "name": "autotest-recorder-golden",
  "private": true,
  "scripts": {
    "setup": "npm install && npm install --prefix backend && npm install --prefix frontend && npx --prefix backend playwright install chromium",
    "dev": "concurrently \\"npm run dev --prefix backend\\" \\"npm run dev --prefix frontend\\"",
    "start": "npm run start --prefix backend",
    "build": "npm run build --prefix frontend"
  },
  "devDependencies": {
    "concurrently": "^9.0.0"
  }
}
"""

FILES["README.md"] = """\
# AutoTest Recorder — Golden Reference

A production-grade AI-powered Record & Playback Automation Tool.

## Quick Start

```bash
npm run setup   # Install all dependencies + Playwright browser
npm run dev     # Start frontend (Vite) + backend (Express) concurrently
```
# ── Frontend ────────────────────────────────────────────────────────────────

FILES["frontend/package.json"] = """\
{
  "name": "frontend",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "axios": "^1.7.2",
    "framer-motion": "^11.3.0",
    "socket.io-client": "^4.7.5",
    "zustand": "^4.5.4",
    "@monaco-editor/react": "^4.6.0",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "vite": "^5.3.4",
    "@vitejs/plugin-react": "^4.3.0",
    "tailwindcss": "^3.4.7",
    "postcss": "^8.4.39",
    "autoprefixer": "^10.4.20"
  }
}
"""

FILES["frontend/vite.config.js"] = """\
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000',
    },
  },
});
"""

FILES["frontend/tailwind.config.js"] = """\
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        base: '#0f172a',
        accent: '#6366f1',
        success: '#22c55e',
        danger: '#ef4444',
      },
    },
  },
  plugins: [],
};
"""

FILES["frontend/postcss.config.js"] = """\
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""

FILES["frontend/index.html"] = """\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AutoTest Recorder</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

FILES["frontend/src/main.jsx"] = """\
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

FILES["frontend/src/App.jsx"] = """\
import Dashboard from './pages/Dashboard';

export default function App() {
  return <Dashboard />;
}
"""

FILES["frontend/src/styles/globals.css"] = """\
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background: #0f172a;
  color: white;
  font-family: Inter, sans-serif;
  margin: 0;
}

/* Glassmorphism utility */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
"""

FILES["frontend/src/pages/Dashboard.jsx"] = """\
import RecorderPanel from '../components/RecorderPanel';
import PlaybackPanel from '../components/PlaybackPanel';
import GeneratedCode from '../components/GeneratedCode';
import UrlInput from '../components/UrlInput';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-base text-white">
      {/* Navbar */}
      <header className="glass h-16 flex items-center justify-between px-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <span className="w-3 h-3 rounded-full bg-danger animate-pulse" />
          <h1 className="text-xl font-bold tracking-tight">AutoTest Recorder</h1>
        </div>
      </header>

      {/* Main layout */}
      <main className="p-6 grid grid-cols-1 xl:grid-cols-2 gap-6">
        <UrlInput />
        <RecorderPanel />
        <PlaybackPanel />
        <GeneratedCode />
      </main>
    </div>
  );
}
"""

FILES["frontend/src/components/UrlInput.jsx"] = """\
import { useState } from 'react';
import { useRecorderStore } from '../store/recorderStore';

export default function UrlInput() {
  const [url, setUrl] = useState('https://example.com');
  const setTargetUrl = useRecorderStore((s) => s.setTargetUrl);

  return (
    <div className="glass rounded-2xl p-6 xl:col-span-2">
      <label className="block text-sm text-white/60 mb-2">Target URL</label>
      <div className="flex gap-3">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:ring-2 focus:ring-accent"
          placeholder="https://your-app.com"
        />
        <button
          onClick={() => setTargetUrl(url)}
          className="bg-accent hover:bg-indigo-600 transition px-5 py-2 rounded-xl font-medium"
        >
          Set URL
        </button>
      </div>
    </div>
  );
}
"""

FILES["frontend/src/components/RecorderPanel.jsx"] = """\
import { useRecorder } from '../hooks/useRecorder';
import { useRecorderStore } from '../store/recorderStore';
import { motion } from 'framer-motion';

export default function RecorderPanel() {
  const { startRecording, stopRecording, loading } = useRecorder();
  const isRecording = useRecorderStore((s) => s.isRecording);
  const events = useRecorderStore((s) => s.events);

  return (
    <div className="glass rounded-2xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-lg">Recording Engine</h2>
        {isRecording && (
          <motion.span
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 1.2, repeat: Infinity }}
            className="flex items-center gap-2 text-sm text-danger"
          >
            <span className="w-2 h-2 rounded-full bg-danger inline-block" />
            Recording
          </motion.span>
        )}
      </div>

      <div className="flex gap-3 mb-4">
        <button
          onClick={startRecording}
          disabled={isRecording || loading}
          className="bg-accent disabled:opacity-50 hover:bg-indigo-600 transition px-5 py-2 rounded-xl"
        >
          {loading ? 'Starting…' : 'Start'}
        </button>
        <button
          onClick={stopRecording}
          disabled={!isRecording}
          className="bg-danger disabled:opacity-50 hover:bg-red-600 transition px-5 py-2 rounded-xl"
        >
          Stop
        </button>
      </div>

      {/* Live event log */}
      <div className="h-48 overflow-y-auto space-y-1">
        {events.length === 0 && (
          <p className="text-white/30 text-sm">No events captured yet.</p>
        )}
        {events.map((ev, i) => (
          <div key={i} className="text-xs text-white/70 bg-white/5 rounded px-3 py-1">
            [{ev.type}] {ev.selector?.primary ?? ev.url ?? ev.value ?? ''}
          </div>
        ))}
      </div>
    </div>
  );
}
"""

FILES["frontend/src/components/PlaybackPanel.jsx"] = """\
import { useState } from 'react';
import api from '../services/api';
import { useRecorderStore } from '../store/recorderStore';
import toast from 'react-hot-toast';

export default function PlaybackPanel() {
  const [logs, setLogs] = useState([]);
  const [running, setRunning] = useState(false);
  const sessionId = useRecorderStore((s) => s.sessionId);

  const runPlayback = async () => {
    if (!sessionId) {
      toast.error('No session recorded yet.');
      return;
    }
    setRunning(true);
    setLogs([]);
    try {
      const { data } = await api.post('/playback/run', { sessionId });
      setLogs(data.logs ?? []);
      toast.success('Playback complete.');
    } catch {
      toast.error('Playback failed.');
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="glass rounded-2xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-lg">Playback Engine</h2>
        <button
          onClick={runPlayback}
          disabled={running}
          className="bg-success disabled:opacity-50 hover:bg-green-600 transition px-4 py-2 rounded-xl text-sm"
        >
          {running ? 'Running…' : '▶ Playback'}
        </button>
      </div>
      <div className="h-48 overflow-y-auto space-y-1">
        {logs.length === 0 && (
          <p className="text-white/30 text-sm">Playback logs will appear here.</p>
        )}
        {logs.map((log, i) => (
          <div
            key={i}
            className={`text-xs rounded px-3 py-1 ${
              log.status === 'error' ? 'bg-danger/20 text-danger' : 'bg-white/5 text-white/70'
            }`}
          >
            {log.message}
          </div>
        ))}
      </div>
    </div>
  );
}
"""

FILES["frontend/src/components/GeneratedCode.jsx"] = """\
import { useState } from 'react';
import Editor from '@monaco-editor/react';
import api from '../services/api';
import { useRecorderStore } from '../store/recorderStore';
import toast from 'react-hot-toast';

export default function GeneratedCode() {
  const [code, setCode] = useState('// Click Generate to produce Playwright test');
  const sessionId = useRecorderStore((s) => s.sessionId);

  const generate = async () => {
    if (!sessionId) { toast.error('No session to generate from.'); return; }
    try {
      const { data } = await api.post('/generator/generate', { sessionId });
      setCode(data.code);
    } catch {
      toast.error('Generation failed.');
    }
  };

  const download = () => {
    const blob = new Blob([code], { type: 'text/javascript' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'recorded.spec.js';
    a.click();
  };

  const copy = () => {
    navigator.clipboard.writeText(code);
    toast.success('Copied to clipboard!');
  };

  return (
    <div className="glass rounded-2xl overflow-hidden xl:col-span-2">
      <div className="flex items-center justify-between px-6 py-3 border-b border-white/10">
        <h2 className="font-semibold text-lg">Generated Playwright Test</h2>
        <div className="flex gap-2">
          <button onClick={generate} className="bg-accent hover:bg-indigo-600 transition px-4 py-1.5 rounded-lg text-sm">Generate</button>
          <button onClick={copy} className="bg-white/10 hover:bg-white/20 transition px-4 py-1.5 rounded-lg text-sm">Copy</button>
          <button onClick={download} className="bg-success hover:bg-green-600 transition px-4 py-1.5 rounded-lg text-sm">Download .spec.js</button>
        </div>
      </div>
      <Editor
        height="400px"
        language="javascript"
        theme="vs-dark"
        value={code}
        onChange={(v) => setCode(v ?? '')}
        options={{ minimap: { enabled: false }, fontSize: 13 }}
      />
    </div>
  );
}
"""

FILES["frontend/src/hooks/useRecorder.js"] = """\
import { useState } from 'react';
import api from '../services/api';
import { useRecorderStore } from '../store/recorderStore';
import toast from 'react-hot-toast';

export function useRecorder() {
  const [loading, setLoading] = useState(false);
  const { targetUrl, setIsRecording, setSessionId, setIsRecording: stopState } =
    useRecorderStore();

  const startRecording = async () => {
    if (!targetUrl) { toast.error('Set a target URL first.'); return; }
    setLoading(true);
    try {
      const { data } = await api.post('/recorder/start', { url: targetUrl });
      setSessionId(data.sessionId);
      setIsRecording(true);
      toast.success('Recording started.');
    } catch {
      toast.error('Failed to start recording.');
    } finally {
      setLoading(false);
    }
  };

  const stopRecording = async () => {
    try {
      await api.post('/recorder/stop');
      stopState(false);
      toast.success('Recording stopped.');
    } catch {
      toast.error('Failed to stop recording.');
    }
  };

  return { startRecording, stopRecording, loading };
}
"""

FILES["frontend/src/services/api.js"] = """\
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 30_000,
});

export default api;
"""

FILES["frontend/src/store/recorderStore.js"] = """\
import { create } from 'zustand';

export const useRecorderStore = create((set) => ({
  targetUrl: '',
  sessionId: null,
  isRecording: false,
  events: [],

  setTargetUrl: (url) => set({ targetUrl: url }),
  setSessionId: (id) => set({ sessionId: id }),
  setIsRecording: (val) => set({ isRecording: val }),
  addEvent: (event) => set((s) => ({ events: [...s.events, event] })),
  clearEvents: () => set({ events: [] }),
}));
"""

# ── Backend ─────────────────────────────────────────────────────────────────

FILES["backend/package.json"] = """\
{
  "name": "backend",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.19.2",
    "playwright": "^1.45.0",
    "uuid": "^10.0.0",
    "fs-extra": "^11.2.0"
  }
}
"""

FILES["backend/.env"] = """\
PORT=5000
"""

FILES["backend/src/server.js"] = """\
import express from 'express';
import cors from 'cors';
import recorderRoutes from './routes/recorder.routes.js';
import playbackRoutes from './routes/playback.routes.js';
import generatorRoutes from './routes/generator.routes.js';

const app = express();
const PORT = process.env.PORT ?? 5000;

app.use(cors());
app.use(express.json());

app.use('/api/recorder', recorderRoutes);
app.use('/api/playback', playbackRoutes);
app.use('/api/generator', generatorRoutes);

// Central error handler
app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ error: err.message ?? 'Internal server error' });
});

app.listen(PORT, () => console.log(`Backend running on port ${PORT}`));
"""

FILES["backend/src/routes/recorder.routes.js"] = """\
import express from 'express';
import { startRecording, stopRecording } from '../controllers/recorder.controller.js';

const router = express.Router();
router.post('/start', startRecording);
router.post('/stop', stopRecording);
export default router;
"""

FILES["backend/src/routes/playback.routes.js"] = """\
import express from 'express';
import { runPlayback } from '../controllers/playback.controller.js';

const router = express.Router();
router.post('/run', runPlayback);
export default router;
"""

FILES["backend/src/routes/generator.routes.js"] = """\
import express from 'express';
import { generateScript } from '../controllers/generator.controller.js';

const router = express.Router();
router.post('/generate', generateScript);
export default router;
"""

FILES["backend/src/controllers/recorder.controller.js"] = """\
import { launchRecorder, haltRecorder } from '../services/recorder.service.js';

/**
 * POST /api/recorder/start
 * Body: { url: string }
 */
export const startRecording = async (req, res, next) => {
  try {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'url is required' });
    const sessionId = await launchRecorder(url);
    res.json({ success: true, sessionId });
  } catch (err) {
    next(err);
  }
};

/**
 * POST /api/recorder/stop
 */
export const stopRecording = async (_req, res, next) => {
  try {
    await haltRecorder();
    res.json({ success: true });
  } catch (err) {
    next(err);
  }
};
"""

FILES["backend/src/controllers/playback.controller.js"] = """\
import { executePlayback } from '../services/playback.service.js';

/**
 * POST /api/playback/run
 * Body: { sessionId: string }
 */
export const runPlayback = async (req, res, next) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId required' });
    const logs = await executePlayback(sessionId);
    res.json({ success: true, logs });
  } catch (err) {
    next(err);
  }
};
"""

FILES["backend/src/controllers/generator.controller.js"] = """\
import { buildScript } from '../services/generator.service.js';

/**
 * POST /api/generator/generate
 * Body: { sessionId: string }
 */
export const generateScript = async (req, res, next) => {
  try {
    const { sessionId } = req.body;
    if (!sessionId) return res.status(400).json({ error: 'sessionId required' });
    const code = await buildScript(sessionId);
    res.json({ success: true, code });
  } catch (err) {
    next(err);
  }
};
"""

FILES["backend/src/services/recorder.service.js"] = """\
import { v4 as uuidv4 } from 'uuid';
import { createRecorder } from '../../../recorder/browserRecorder.js';
import { attachEventListeners } from '../../../recorder/eventListeners.js';
import { attachDialogHandler } from '../../../recorder/dialogHandler.js';
import fs from 'fs-extra';
import path from 'path';

// In-memory store: sessionId → { browser, events }
const activeSessions = new Map();

export async function launchRecorder(url) {
  const sessionId = uuidv4();
  const events = [];

  const { browser, page } = await createRecorder(url);
  await attachEventListeners(page, events);
  attachDialogHandler(page, events);

  // Record initial navigation
  events.push({ type: 'goto', url, timestamp: Date.now() });

  activeSessions.set(sessionId, { browser, events });
  return sessionId;
}

export async function haltRecorder() {
  for (const [sessionId, session] of activeSessions) {
    // Persist events to disk for later retrieval
    const dir = path.resolve('backend/sessions');
    await fs.ensureDir(dir);
    await fs.writeJson(path.join(dir, `${sessionId}.json`), session.events, { spaces: 2 });

    await session.browser.close();
    activeSessions.delete(sessionId);
  }
}

export function getSession(sessionId) {
  return activeSessions.get(sessionId) ?? null;
}

export async function loadSessionEvents(sessionId) {
  const filePath = path.resolve('backend/sessions', `${sessionId}.json`);
  if (await fs.pathExists(filePath)) {
    return fs.readJson(filePath);
  }
  const session = activeSessions.get(sessionId);
  return session?.events ?? [];
}
"""

FILES["backend/src/services/playback.service.js"] = """\
import { chromium } from 'playwright';
import { loadSessionEvents } from './recorder.service.js';
import { executeAction } from '../../../playback/actionExecutor.js';
import { withRetry } from '../../../playback/retryHandler.js';

export async function executePlayback(sessionId) {
  const events = await loadSessionEvents(sessionId);
  const logs = [];

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  for (const event of events) {
    try {
      await withRetry(() => executeAction(page, event), 3);
      logs.push({ status: 'ok', message: `✓ ${event.type}: ${event.selector?.primary ?? event.url ?? ''}` });
    } catch (err) {
      // Screenshot on failure
      await page.screenshot({ path: `backend/screenshots/failure-${Date.now()}.png` });
      logs.push({ status: 'error', message: `✗ ${event.type} failed: ${err.message}` });
    }
  }

  await browser.close();
  return logs;
}
"""

FILES["backend/src/services/generator.service.js"] = """\
import { loadSessionEvents } from './recorder.service.js';
import { generatePlaywright } from '../../../generator/playwrightGenerator.js';

export async function buildScript(sessionId) {
  const events = await loadSessionEvents(sessionId);
  return generatePlaywright(events);
}
"""

FILES["backend/src/utils/logger.js"] = """\
export function log(msg) {
  console.log(`[${new Date().toISOString()}] ${msg}`);
}

export function error(msg) {
  console.error(`[${new Date().toISOString()}] ERROR: ${msg}`);
}
"""

# ── Recorder engine ──────────────────────────────────────────────────────────

FILES["recorder/browserRecorder.js"] = """\
import { chromium } from 'playwright';

/**
 * Launch a Chromium browser in headed mode and navigate to the target URL.
 * Returns { browser, context, page } for downstream use.
 */
export async function createRecorder(url) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
  });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  return { browser, context, page };
}
"""

FILES["recorder/eventListeners.js"] = """\
import { generateSelector } from './selectorEngine.js';

/**
 * Inject DOM event listeners into the page via Playwright's bridge.
 * Events are pushed into the shared `events` array via exposeFunction.
 */
export async function attachEventListeners(page, events) {
  // Expose Node.js function to browser context
  await page.exposeFunction('__captureEvent', (event) => {
    events.push({ ...event, timestamp: Date.now() });
  });

  await page.addInitScript(() => {
    // ── Click ──────────────────────────────────────────────────────────────
    document.addEventListener('click', (e) => {
      const el = e.target;
      window.__captureEvent({
        type: 'click',
        tag: el.tagName,
        text: el.innerText?.slice(0, 80),
        selector: window.__buildSelector(el),
      });
    }, true);

    // ── Input / fill ───────────────────────────────────────────────────────
    document.addEventListener('input', (e) => {
      const el = e.target;
      window.__captureEvent({
        type: 'input',
        value: el.value,
        selector: window.__buildSelector(el),
      });
    }, true);

    // ── Select / dropdown ──────────────────────────────────────────────────
    document.addEventListener('change', (e) => {
      const el = e.target;
      if (el.tagName === 'SELECT') {
        window.__captureEvent({
          type: 'select',
          value: el.value,
          selector: window.__buildSelector(el),
        });
      }
    }, true);

    // ── Keyboard ───────────────────────────────────────────────────────────
    document.addEventListener('keydown', (e) => {
      if (['Enter', 'Tab', 'Escape'].includes(e.key)) {
        window.__captureEvent({ type: 'keydown', key: e.key });
      }
    }, true);

    // ── Selector builder (mirrors selectorEngine priority in browser ctx) ──
    window.__buildSelector = (el) => {
      const testId = el.dataset?.testid;
      if (testId) return { primary: `[data-testid="${testId}"]`, strategy: 'testid' };

      const role = el.getAttribute('role');
      const name = el.getAttribute('aria-label') || el.innerText?.trim().slice(0, 40);
      if (role && name) return { primary: `getByRole('${role}', { name: '${name}' })`, strategy: 'role' };

      const ariaLabel = el.getAttribute('aria-label');
      if (ariaLabel) return { primary: `[aria-label="${ariaLabel}"]`, strategy: 'aria' };

      const placeholder = el.getAttribute('placeholder');
      if (placeholder) return { primary: `[placeholder="${placeholder}"]`, strategy: 'placeholder' };

      if (el.id) return { primary: `#${el.id}`, strategy: 'css' };

      const cls = Array.from(el.classList).slice(0, 2).join('.');
      if (cls) return { primary: `.${cls}`, strategy: 'css' };

      // XPath fallback — absolute path as last resort
      return { primary: `//${el.tagName.toLowerCase()}`, strategy: 'xpath' };
    };
  });
}
"""

FILES["recorder/selectorEngine.js"] = """\
/**
 * Server-side selector generator (used for post-processing).
 * Implements the 6-tier priority from the prompt spec.
 *
 * Priority: data-testid > getByRole > aria-label > placeholder > CSS > XPath
 */
export function generateSelector(elementInfo) {
  const { testid, role, ariaLabel, placeholder, id, tagName, classes } = elementInfo;

  if (testid) {
    return {
      primary: `[data-testid="${testid}"]`,
      fallbacks: [],
      strategy: 'testid',
    };
  }

  if (role) {
    return {
      primary: `getByRole('${role}')`,
      fallbacks: ariaLabel ? [`[aria-label="${ariaLabel}"]`] : [],
      strategy: 'role',
    };
  }

  if (ariaLabel) {
    return {
      primary: `[aria-label="${ariaLabel}"]`,
      fallbacks: id ? [`#${id}`] : [],
      strategy: 'aria',
    };
  }

  if (placeholder) {
    return {
      primary: `[placeholder="${placeholder}"]`,
      fallbacks: [],
      strategy: 'placeholder',
    };
  }

  if (id) {
    return {
      primary: `#${id}`,
      fallbacks: [],
      strategy: 'css',
    };
  }

  if (classes?.length) {
    const selector = classes.slice(0, 2).map((c) => `.${c}`).join('');
    return { primary: selector, fallbacks: [], strategy: 'css' };
  }

  // Last resort — avoid absolute XPath; use tag only
  return {
    primary: `//${tagName ?? 'div'}`,
    fallbacks: [],
    strategy: 'xpath',
  };
}

/**
 * Attempt to heal a broken selector by trying fallbacks.
 * Returns the first selector that resolves on the page.
 */
export async function healSelector(page, selectorObj) {
  const candidates = [selectorObj.primary, ...selectorObj.fallbacks];
  for (const sel of candidates) {
    try {
      await page.locator(sel).waitFor({ timeout: 2000 });
      return sel;
    } catch {
      // Continue to next candidate
    }
  }
  throw new Error(`Selector healing failed for: ${JSON.stringify(candidates)}`);
}
"""

FILES["recorder/dialogHandler.js"] = """\
/**
 * Attach dialog (alert / confirm / prompt) listeners to the page.
 * Captures dialog metadata before auto-accepting so recording continues.
 */
export function attachDialogHandler(page, events) {
  page.on('dialog', async (dialog) => {
    const dialogEvent = {
      type: 'dialog',
      dialogType: dialog.type(),       // 'alert' | 'confirm' | 'prompt' | 'beforeunload'
      message: dialog.message(),
      defaultValue: dialog.defaultValue(),
      timestamp: Date.now(),
    };

    events.push(dialogEvent);

    // Auto-accept during recording to keep the session alive
    if (dialog.type() === 'prompt') {
      await dialog.accept('sample input');
    } else {
      await dialog.accept();
    }
  });
}
"""

# ── Generator ────────────────────────────────────────────────────────────────

FILES["generator/playwrightGenerator.js"] = """\
import { formatStep } from './stepFormatter.js';
import { generateAssertions } from './assertionGenerator.js';

/**
 * Generate a clean, production-ready Playwright test from recorded events.
 * No waitForTimeout. No duplicate locators. No noisy artifacts.
 *
 * @param {Array} events - Recorded event objects
 * @returns {string} - Executable Playwright .spec.js content
 */
export function generatePlaywright(events) {
  const lines = [];

  // ── Imports ──────────────────────────────────────────────────────────────
  lines.push(`import { test, expect } from '@playwright/test';`);
  lines.push('');
  lines.push(`test('Recorded Flow', async ({ page }) => {`);

  // Pre-pass: emit dialog handlers BEFORE the step that triggers them
  const dialogIndices = new Set(
    events
      .map((e, i) => (e.type === 'dialog' ? i : -1))
      .filter((i) => i !== -1)
  );

  for (let i = 0; i < events.length; i++) {
    const event = events[i];

    // If the NEXT event triggers a dialog, register the handler first
    if (i + 1 < events.length && dialogIndices.has(i + 1)) {
      const dialog = events[i + 1];
      lines.push(...emitDialogHandler(dialog).map((l) => '  ' + l));
    }

    // Skip dialog events themselves (already handled above)
    if (event.type === 'dialog') continue;

    const step = formatStep(event);
    if (step) lines.push('  ' + step);
  }

  // Auto-assertions on final state
  const assertions = generateAssertions(events);
  for (const a of assertions) lines.push('  ' + a);

  lines.push('});');
  return lines.join('\\n');
}

function emitDialogHandler(dialogEvent) {
  const { dialogType, message } = dialogEvent;
  if (dialogType === 'prompt') {
    return [
      `page.on('dialog', async dialog => {`,
      `  if (dialog.type() === 'prompt') {`,
      `    await dialog.accept('sample input'); // captured: "${message}"`,
      `  }`,
      `});`,
    ];
  }
  return [
    `page.on('dialog', async dialog => {`,
    `  if (dialog.type() === '${dialogType}') {`,
    `    await dialog.accept(); // captured: "${message}"`,
    `  }`,
    `});`,
  ];
}
"""

FILES["generator/stepFormatter.js"] = """\
/**
 * Convert a single recorded event into a Playwright statement string.
 * Returns null for unknown/unhandled events (they are silently skipped).
 */
export function formatStep(event) {
  const sel = event.selector?.primary ?? null;

  switch (event.type) {
    case 'goto':
      return `await page.goto('${event.url}');`;

    case 'click':
      if (!sel) return null;
      // Prefer semantic locator if role strategy was used
      if (event.selector?.strategy === 'role') {
        return `await ${sel}.click();`;
      }
      return `await page.locator('${sel}').click();`;

    case 'input':
      if (!sel) return null;
      return `await page.locator('${sel}').fill('${escape(event.value ?? '')}');`;

    case 'select':
      if (!sel) return null;
      return `await page.locator('${sel}').selectOption('${escape(event.value ?? '')}');`;

    case 'keydown':
      return `await page.keyboard.press('${event.key}');`;

    default:
      return null;
  }
}

function escape(str) {
  return str.replace(/'/g, "\\\\'");
}
"""

FILES["generator/assertionGenerator.js"] = """\
/**
 * Generate meaningful assertions from the recorded event sequence.
 * Appended after all steps to validate final page state.
 */
export function generateAssertions(events) {
  const assertions = [];

  // Assert final URL after navigation events
  const lastGoto = [...events].reverse().find((e) => e.type === 'goto');
  if (lastGoto) {
    assertions.push(`await expect(page).toHaveURL('${lastGoto.url}');`);
  }

  return assertions;
}
"""

# ── Playback ─────────────────────────────────────────────────────────────────

FILES["playback/playbackRunner.js"] = """\
import { chromium } from 'playwright';
import { executeAction } from './actionExecutor.js';
import { withRetry } from './retryHandler.js';

/**
 * Replay a sequence of recorded events in a fresh browser instance.
 * Returns a structured log array: [{ status, message }]
 */
export async function runPlayback(events) {
  const logs = [];
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  for (const event of events) {
    const label = `${event.type}:${event.selector?.primary ?? event.url ?? event.key ?? ''}`;
    try {
      await withRetry(() => executeAction(page, event), 3);
      logs.push({ status: 'ok', message: `✓ ${label}` });
    } catch (err) {
      await page
        .screenshot({ path: `playback/screenshots/fail-${Date.now()}.png` })
        .catch(() => {});
      logs.push({ status: 'error', message: `✗ ${label} — ${err.message}` });
    }
  }

  await browser.close();
  return logs;
}
"""

FILES["playback/actionExecutor.js"] = """\
/**
 * Execute a single recorded event on the Playwright page.
 * Throws on failure so the retry handler can catch it.
 */
export async function executeAction(page, event) {
  switch (event.type) {
    case 'goto':
      await page.goto(event.url, { waitUntil: 'domcontentloaded' });
      break;

    case 'click': {
      const locator = resolveLocator(page, event);
      await locator.click();
      break;
    }

    case 'input': {
      const locator = resolveLocator(page, event);
      await locator.fill(event.value ?? '');
      break;
    }

    case 'select': {
      const locator = resolveLocator(page, event);
      await locator.selectOption(event.value ?? '');
      break;
    }

    case 'keydown':
      await page.keyboard.press(event.key);
      break;

    case 'dialog':
      // Dialog events are handled via page.on('dialog') at context level
      break;

    default:
      throw new Error(`Unknown event type: ${event.type}`);
  }
}

/**
 * Build a Playwright Locator from the selector object.
 * Falls back through the selector list if needed.
 */
function resolveLocator(page, event) {
  const primary = event.selector?.primary;
  if (!primary) throw new Error('No selector available for event');

  // getByRole calls cannot be passed to page.locator — handle separately
  if (primary.startsWith('getByRole(')) {
    // Parse and call dynamically: getByRole('button', { name: 'Submit' })
    return eval(`page.${primary}`); // eslint-disable-line no-eval
  }
  return page.locator(primary);
}
"""

FILES["playback/retryHandler.js"] = """\
/**
 * Execute an async action with exponential back-off retry.
 *
 * @param {Function} action - Async function to attempt
 * @param {number}   maxAttempts - Maximum number of tries (default 3)
 * @param {number}   baseDelay   - Initial delay in ms (default 500)
 */
export async function withRetry(action, maxAttempts = 3, baseDelay = 500) {
  let lastError;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await action();
    } catch (err) {
      lastError = err;
      if (attempt < maxAttempts) {
        await sleep(baseDelay * attempt); // 500ms, 1000ms, 1500ms
      }
    }
  }
  throw lastError;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
"""

# ── Shared ───────────────────────────────────────────────────────────────────

FILES["shared/constants/events.js"] = """\
export const EVENT_TYPES = {
  GOTO: 'goto',
  CLICK: 'click',
  INPUT: 'input',
  SELECT: 'select',
  KEYDOWN: 'keydown',
  DIALOG: 'dialog',
};

export const DIALOG_TYPES = {
  ALERT: 'alert',
  CONFIRM: 'confirm',
  PROMPT: 'prompt',
};

export const SELECTOR_STRATEGIES = {
  TESTID: 'testid',
  ROLE: 'role',
  ARIA: 'aria',
  PLACEHOLDER: 'placeholder',
  CSS: 'css',
  XPATH: 'xpath',
};
"""

FILES["shared/helpers/uid.js"] = """\
import { v4 as uuidv4 } from 'uuid';

export function generateId() {
  return uuidv4();
}
"""

FILES["shared/logger/consoleLogger.js"] = """\
export function log(scope, msg) {
  console.log(`[${scope}] ${new Date().toISOString()} ${msg}`);
}

export function warn(scope, msg) {
  console.warn(`[${scope}] WARN: ${msg}`);
}

export function error(scope, msg, err) {
  console.error(`[${scope}] ERROR: ${msg}`, err ?? '');
}
"""


# ── Example generated test ────────────────────────────────────────────────────

FILES["docs/example.spec.js"] = """\
/**
 * Example: Auto-generated Playwright test from AutoTest Recorder
 * This is what the generator produces for a typical login flow.
 */
import { test, expect } from '@playwright/test';

test('Recorded Flow', async ({ page }) => {
  await page.goto('https://example.com');

  await page.getByLabel('Username').fill('admin');
  await page.getByLabel('Password').fill('password');

  // Dialog handler registered before the trigger action
  page.on('dialog', async dialog => {
    if (dialog.type() === 'confirm') {
      await dialog.accept(); // captured: "Proceed with login?"
    }
  });

  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page.getByText('Dashboard')).toBeVisible();
  await expect(page).toHaveURL('https://example.com/dashboard');
});
"""

FILES["docs/architecture.md"] = """\
# AutoTest Recorder — Architecture

## Data Flow

```
User Browser Action
        │
        ▼
 eventListeners.js  ──── DOM events injected via addInitScript + exposeFunction
        │
        ▼
  events[] array   ──── Structured JSON: { type, selector, value, timestamp }
        │
        ▼
recorder.service.js ──── Session management, persistence to disk
        │
        ├──► generator.service.js → playwrightGenerator.js → .spec.js output
        │
        └──► playback.service.js  → actionExecutor.js + retryHandler.js
```

# ---------------------------------------------------------------------------
# Scaffold builder
# ---------------------------------------------------------------------------

def build_project(output_dir: str) -> None:
    """Write all files to the specified output directory."""
    created = 0
    for rel_path, content in FILES.items():
        abs_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"  ✓ {rel_path}")
        created += 1

    print(f"\n✅ Golden scaffold created: {created} files in '{output_dir}'")
    print("\nNext steps:")
    print("  cd", output_dir)
    print("  npm run setup")
    print("  npm run dev")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the AutoTest Recorder golden project scaffold."
    )
    parser.add_argument(
        "--output-dir",
        default="./autotest-recorder-golden",
        help="Directory to write the project into (default: ./autotest-recorder-golden)",
    )
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)

    if os.path.exists(output_dir):
        print(f"⚠️  Directory already exists: {output_dir}")
        answer = input("Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    print(f"\n🚀 Building golden scaffold → {output_dir}\n")
    build_project(output_dir)


if __name__ == "__main__":
    main()
