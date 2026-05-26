import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { generatePlaywright } from '../../generator/playwrightGenerator.js';

const app = express();
const port = process.env.PORT || 5000;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDist = path.resolve(__dirname, '../../frontend/dist');

app.use(express.json({ limit: '1mb' }));

const recorderClientScript = String.raw`
(() => {
  if (window.__AUTOTEST_RECORDER__) return;
  window.__AUTOTEST_RECORDER__ = true;

  const textSelector = (text) => {
    const clean = String(text || '').replace(/\s+/g, ' ').trim();
    return clean && clean.length < 80 ? 'text=' + clean : '';
  };

  const cssEscape = (value) => {
    if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
    return String(value).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
  };

  const selectorFor = (element) => {
    if (!element || element === document.body) return 'body';
    if (element.id) return '#' + cssEscape(element.id);

    const testId = element.getAttribute('data-testid') || element.getAttribute('data-test');
    if (testId) return '[data-testid="' + testId.replace(/"/g, '\\"') + '"]';

    const aria = element.getAttribute('aria-label');
    if (aria) return '[aria-label="' + aria.replace(/"/g, '\\"') + '"]';

    if (element.name) return element.tagName.toLowerCase() + '[name="' + element.name.replace(/"/g, '\\"') + '"]';

    if (['A', 'BUTTON'].includes(element.tagName)) {
      const byText = textSelector(element.innerText);
      if (byText) return byText;
    }

    const parts = [];
    let node = element;
    while (node && node.nodeType === Node.ELEMENT_NODE && node !== document.body) {
      let part = node.tagName.toLowerCase();
      const parent = node.parentElement;
      if (!parent) break;
      const siblings = [...parent.children].filter((item) => item.tagName === node.tagName);
      if (siblings.length > 1) part += ':nth-of-type(' + (siblings.indexOf(node) + 1) + ')';
      parts.unshift(part);
      node = parent;
      if (parts.length >= 4) break;
    }

    return parts.join(' > ') || element.tagName.toLowerCase();
  };

  const findBySelector = (selector) => {
    if (!selector) return null;
    if (selector.startsWith('text=')) {
      const wanted = selector.slice(5).trim().toLowerCase();
      return [...document.querySelectorAll('button,a,input,textarea,select,[role="button"],body *')]
        .find((element) => (element.innerText || element.value || '').trim().toLowerCase().includes(wanted));
    }
    try {
      return document.querySelector(selector);
    } catch {
      return null;
    }
  };

  const post = (payload) => {
    window.parent.postMessage({ source: 'autotest-recorder-frame', ...payload }, '*');
  };

  const highlight = (element, ok = true) => {
    if (!element) return;
    const previous = element.style.outline;
    element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
    element.style.outline = ok ? '3px solid #0f766e' : '3px solid #dc2626';
    window.setTimeout(() => {
      element.style.outline = previous;
    }, 900);
  };

  document.addEventListener('click', (event) => {
    const element = event.target.closest('a,button,input,textarea,select,[role="button"]') || event.target;
    const anchor = event.target.closest('a[href]');
    post({
      event: 'record-step',
      step: {
        type: 'click',
        selector: selectorFor(element),
        text: (element.innerText || element.value || '').trim().slice(0, 120)
      }
    });

    if (anchor && anchor.href) {
      event.preventDefault();
      post({ event: 'navigate', url: anchor.href });
    }
  }, true);

  document.addEventListener('change', (event) => {
    const element = event.target;
    if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(element.tagName)) return;
    post({
      event: 'record-step',
      step: {
        type: 'fill',
        selector: selectorFor(element),
        value: element.value
      }
    });
  }, true);

  document.addEventListener('keydown', (event) => {
    if (!['Enter', 'Tab', 'Escape'].includes(event.key)) return;
    post({
      event: 'record-step',
      step: {
        type: 'press',
        selector: selectorFor(event.target),
        value: event.key
      }
    });
  }, true);

  window.addEventListener('message', async (event) => {
    const message = event.data || {};
    if (message.source !== 'autotest-recorder-app' || message.event !== 'play-step') return;

    const step = message.step || {};
    const element = findBySelector(step.selector);

    try {
      if (step.type === 'click') {
        if (!element) throw new Error('Element not found');
        highlight(element);
        element.click();
      }

      if (step.type === 'fill') {
        if (!element) throw new Error('Element not found');
        highlight(element);
        element.focus();
        element.value = step.value || '';
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
      }

      if (step.type === 'press') {
        if (!element) throw new Error('Element not found');
        highlight(element);
        element.focus();
        element.dispatchEvent(new KeyboardEvent('keydown', { key: step.value || 'Enter', bubbles: true }));
      }

      if (step.type === 'expectVisible') {
        if (!element) throw new Error('Element not found');
        highlight(element);
      }

      if (step.type === 'expectText') {
        if (!element || !String(element.innerText || element.value || '').includes(step.value || '')) {
          throw new Error('Expected text not found');
        }
        highlight(element);
      }

      post({ event: 'play-result', ok: true, stepId: step.id });
    } catch (error) {
      if (element) highlight(element, false);
      post({ event: 'play-result', ok: false, stepId: step.id, error: error.message });
    }
  });

  post({ event: 'ready', title: document.title });
})();
`;

function injectRecorder(html, targetUrl) {
  const injection = `<base href="${targetUrl}"><script>${recorderClientScript}</script>`;
  if (html.includes('</head>')) return html.replace('</head>', () => `${injection}</head>`);
  return `${injection}${html}`;
}

app.get('/api/health', (req, res) => {
  res.json({ status: 'running' });
});

app.post('/api/generate', (req, res) => {
  const steps = Array.isArray(req.body?.steps) ? req.body.steps : [];
  const name = req.body?.name || 'recorded flow';

  res.json({
    code: generatePlaywright(steps, { name })
  });
});

app.get('/api/proxy', async (req, res) => {
  try {
    const targetUrl = new URL(req.query.url);
    if (!['http:', 'https:'].includes(targetUrl.protocol)) {
      res.status(400).send('Only http and https URLs are supported.');
      return;
    }

    const response = await fetch(targetUrl, {
      headers: {
        'user-agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
      }
    });
    const contentType = response.headers.get('content-type') || 'text/html';

    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Content-Type', contentType);

    if (!contentType.includes('text/html')) {
      const body = Buffer.from(await response.arrayBuffer());
      res.send(body);
      return;
    }

    const html = await response.text();
    res.send(injectRecorder(html, targetUrl.href));
  } catch (error) {
    res.status(400).send(`Could not load URL: ${error.message}`);
  }
});

app.use(express.static(frontendDist));

app.use((req, res) => {
  res.sendFile(path.join(frontendDist, 'index.html'));
});

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});
