import React, { useEffect, useMemo, useRef, useState } from 'react';

const STORAGE_KEY = 'autotest-recorder-session';

const stepTypes = [
  { value: 'goto', label: 'Go to URL' },
  { value: 'click', label: 'Click' },
  { value: 'fill', label: 'Fill' },
  { value: 'press', label: 'Press key' },
  { value: 'expectText', label: 'Expect text' },
  { value: 'expectVisible', label: 'Expect visible' }
];

function normalizeUrl(value) {
  const trimmed = value.trim();
  if (!trimmed) return '';
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  return `https://${trimmed}`;
}

function generateCode(steps, name) {
  const quote = (value = '') => JSON.stringify(String(value));
  const stepLines = steps.map((step) => {
    if (step.type === 'goto') return `  await page.goto(${quote(step.url)});`;
    if (step.type === 'click') return `  await page.locator(${quote(step.selector)}).click();`;
    if (step.type === 'fill') {
      return `  await page.locator(${quote(step.selector)}).fill(${quote(step.value)});`;
    }
    if (step.type === 'press') {
      return `  await page.locator(${quote(step.selector)}).press(${quote(step.value || 'Enter')});`;
    }
    if (step.type === 'expectText') {
      return `  await expect(page.locator(${quote(step.selector)})).toContainText(${quote(step.value)});`;
    }
    if (step.type === 'expectVisible') {
      return `  await expect(page.locator(${quote(step.selector)})).toBeVisible();`;
    }
    return `  // Unsupported step: ${quote(step.type)}`;
  });

  return `import { test, expect } from '@playwright/test';

test(${quote(name || 'recorded flow')}, async ({ page }) => {
${stepLines.length ? stepLines.join('\n') : '  // Record steps, then copy or download this test.'}
});
`;
}

function makeStep(step) {
  return {
    id: crypto.randomUUID(),
    type: step.type || 'click',
    url: step.url || '',
    selector: step.selector || '',
    value: step.value || '',
    text: step.text || ''
  };
}

export default function App() {
  const frameRef = useRef(null);
  const playbackTimerRef = useRef(null);
  const [testName, setTestName] = useState('recorded flow');
  const [targetUrl, setTargetUrl] = useState('https://example.com');
  const [frameUrl, setFrameUrl] = useState('');
  const [steps, setSteps] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeStepId, setActiveStepId] = useState('');
  const [message, setMessage] = useState('');

  const generatedCode = useMemo(() => generateCode(steps, testName), [steps, testName]);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;

    try {
      const session = JSON.parse(saved);
      setTestName(session.testName || 'recorded flow');
      setTargetUrl(session.targetUrl || 'https://example.com');
      setSteps(Array.isArray(session.steps) ? session.steps : []);
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ testName, targetUrl, steps }));
  }, [testName, targetUrl, steps]);

  useEffect(() => {
    function handleMessage(event) {
      const payload = event.data || {};
      if (payload.source !== 'autotest-recorder-frame') return;

      if (payload.event === 'record-step' && isRecording && !isPlaying) {
        setSteps((current) => [...current, makeStep(payload.step)]);
      }

      if (payload.event === 'navigate' && payload.url) {
        loadUrl(payload.url, true);
      }

      if (payload.event === 'ready' && payload.title) {
        showMessage(`Loaded: ${payload.title}`);
      }

      if (payload.event === 'play-result' && !payload.ok) {
        showMessage(payload.error || 'Playback step failed.');
      }
    }

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [isRecording, isPlaying]);

  function showMessage(text) {
    setMessage(text);
    window.clearTimeout(playbackTimerRef.current);
    playbackTimerRef.current = window.setTimeout(() => setMessage(''), 2400);
  }

  function proxyUrl(url) {
    return `/api/proxy?url=${encodeURIComponent(url)}&t=${Date.now()}`;
  }

  function loadUrl(url, recordNavigation = false) {
    const nextUrl = normalizeUrl(url);
    if (!nextUrl) {
      showMessage('Enter a URL to start recording.');
      return;
    }

    setTargetUrl(nextUrl);
    setFrameUrl(proxyUrl(nextUrl));

    if (recordNavigation) {
      setSteps((current) => [...current, makeStep({ type: 'goto', url: nextUrl })]);
    }
  }

  function startRecording() {
    const nextUrl = normalizeUrl(targetUrl);
    if (!nextUrl) {
      showMessage('Enter a URL to start recording.');
      return;
    }

    setIsRecording(true);
    setIsPlaying(false);
    setFrameUrl(proxyUrl(nextUrl));
    setSteps((current) => {
      if (current[0]?.type === 'goto' && current[0]?.url === nextUrl) return current;
      return [makeStep({ type: 'goto', url: nextUrl }), ...current];
    });
  }

  function updateStep(id, field, value) {
    setSteps((current) =>
      current.map((step) => (step.id === id ? { ...step, [field]: value } : step))
    );
  }

  function moveStep(id, direction) {
    setSteps((current) => {
      const index = current.findIndex((step) => step.id === id);
      const nextIndex = index + direction;
      if (index < 0 || nextIndex < 0 || nextIndex >= current.length) return current;
      const updated = [...current];
      [updated[index], updated[nextIndex]] = [updated[nextIndex], updated[index]];
      return updated;
    });
  }

  function removeStep(id) {
    setSteps((current) => current.filter((step) => step.id !== id));
  }

  function addAssertion(type) {
    setSteps((current) => [
      ...current,
      makeStep({
        type,
        selector: 'h1',
        value: type === 'expectText' ? 'Example Domain' : ''
      })
    ]);
  }

  async function copyCode() {
    await navigator.clipboard.writeText(generatedCode);
    showMessage('Playwright code copied.');
  }

  function downloadCode() {
    const blob = new Blob([generatedCode], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${testName.toLowerCase().replace(/[^a-z0-9]+/g, '-') || 'test'}.spec.js`;
    link.click();
    URL.revokeObjectURL(url);
  }

  async function playSteps() {
    if (!steps.length) {
      showMessage('Record or add steps before playback.');
      return;
    }

    setIsPlaying(true);
    setIsRecording(false);

    for (const step of steps) {
      setActiveStepId(step.id);

      if (step.type === 'goto') {
        setTargetUrl(step.url);
        setFrameUrl(proxyUrl(step.url));
        await new Promise((resolve) => window.setTimeout(resolve, 1400));
        continue;
      }

      frameRef.current?.contentWindow?.postMessage(
        { source: 'autotest-recorder-app', event: 'play-step', step },
        '*'
      );
      await new Promise((resolve) => window.setTimeout(resolve, 900));
    }

    setActiveStepId('');
    setIsPlaying(false);
    showMessage('Playback finished.');
  }

  function clearSession() {
    setSteps([]);
    setActiveStepId('');
    setIsPlaying(false);
    setIsRecording(false);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AutoTest Recorder</p>
          <h1>Record, edit, and replay browser flows</h1>
        </div>
        <div className="topbar-actions">
          <button type="button" className="ghost-button" onClick={playSteps}>
            Playback
          </button>
          <button type="button" className="primary-button" onClick={copyCode}>
            Copy code
          </button>
        </div>
      </header>

      <main className="recorder-layout">
        <section className="panel browser-panel" aria-label="Website recorder">
          <div className="urlbar">
            <input
              value={targetUrl}
              onChange={(event) => setTargetUrl(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') startRecording();
              }}
              placeholder="https://example.com"
            />
            <button type="button" className="primary-button" onClick={startRecording}>
              {isRecording ? 'Recording' : 'Record'}
            </button>
            <button type="button" className="ghost-button" onClick={() => loadUrl(targetUrl)}>
              Load
            </button>
          </div>

          <div className="recorder-status">
            <span className={isRecording ? 'status-dot active' : 'status-dot'} />
            <span>{isRecording ? 'Recording interactions' : 'Paused'}</span>
            <span>{steps.length} steps captured</span>
          </div>

          <div className="browser-frame-wrap">
            {frameUrl ? (
              <iframe ref={frameRef} title="Recorded website" src={frameUrl} />
            ) : (
              <div className="empty-browser">Enter a URL, then press Record.</div>
            )}
          </div>
        </section>

        <aside className="panel steps-panel" aria-label="Editable automation steps">
          <div className="panel-heading">
            <h2>Editable steps</h2>
            <div className="inline-actions">
              <button type="button" onClick={() => addAssertion('expectVisible')}>
                + Visible
              </button>
              <button type="button" onClick={() => addAssertion('expectText')}>
                + Text
              </button>
            </div>
          </div>

          <div className="step-list">
            {steps.length === 0 ? (
              <p className="empty-state">Interactions you perform in the website frame will appear here.</p>
            ) : (
              steps.map((step, index) => (
                <article
                  className={activeStepId === step.id ? 'step-item active-step' : 'step-item'}
                  key={step.id}
                >
                  <span className="step-index">{index + 1}</span>
                  <div className="step-editor">
                    <select value={step.type} onChange={(event) => updateStep(step.id, 'type', event.target.value)}>
                      {stepTypes.map((type) => (
                        <option key={type.value} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </select>

                    {step.type === 'goto' ? (
                      <input
                        value={step.url}
                        onChange={(event) => updateStep(step.id, 'url', event.target.value)}
                        placeholder="URL"
                      />
                    ) : (
                      <input
                        value={step.selector}
                        onChange={(event) => updateStep(step.id, 'selector', event.target.value)}
                        placeholder="Selector"
                      />
                    )}

                    {['fill', 'press', 'expectText'].includes(step.type) && (
                      <input
                        value={step.value}
                        onChange={(event) => updateStep(step.id, 'value', event.target.value)}
                        placeholder="Value"
                      />
                    )}
                  </div>
                  <div className="step-actions">
                    <button type="button" onClick={() => moveStep(step.id, -1)}>
                      Up
                    </button>
                    <button type="button" onClick={() => moveStep(step.id, 1)}>
                      Down
                    </button>
                    <button type="button" onClick={() => removeStep(step.id)}>
                      Delete
                    </button>
                  </div>
                </article>
              ))
            )}
          </div>
        </aside>

        <section className="panel output-panel" aria-label="Generated Playwright code">
          <div className="panel-heading">
            <div>
              <h2>Generated Playwright test</h2>
              <input value={testName} onChange={(event) => setTestName(event.target.value)} />
            </div>
            <div className="inline-actions">
              <button type="button" onClick={downloadCode}>
                Download
              </button>
              <button type="button" onClick={clearSession}>
                Clear
              </button>
            </div>
          </div>
          <pre>
            <code>{generatedCode}</code>
          </pre>
        </section>
      </main>

      {message && <div className="toast">{message}</div>}
    </div>
  );
}
