# Prompt: AI-Powered Record & Playback Automation Tool

**Domain:** DevOps / QA Automation / SaaS Engineering  
**Author:** Piyush Chauhan  
**Complexity Level:** Senior Full-Stack / Production-Grade

---

## Task Description

Act as a senior full-stack engineer and UI/UX architect building a **production-grade, AI-powered Record & Playback Automation Tool**.

The goal is to create a modern web application that:
- Records real browser interactions
- Automatically generates clean, executable Playwright test scripts
- Plays back recorded sessions with visual feedback
- Exports professional `.spec.js` files ready for CI/CD pipelines

The final product must be a real **SaaS-quality automation platform** — modern, responsive, smooth, reliable, maintainable, and production-ready.

---

## Explicit Constraints (All Must Be Satisfied)

### Constraint 1 — Tech Stack (Non-Negotiable)
- **Frontend:** React + Tailwind CSS + Framer Motion
- **Backend:** Node.js + Express.js
- **Automation:** Playwright
- **Optional:** WebSocket (live logs), Monaco Editor (code preview)

### Constraint 2 — Recording Engine Must Capture
- Clicks, inputs, dropdown selections, checkbox interactions
- Navigation events, page transitions, keyboard actions
- JavaScript dialogs: `alert()`, `confirm()`, `prompt()`
- All events stored in structured JSON format:

```json
{
  "type": "click",
  "selector": {
    "primary": "getByRole('button')",
    "fallbacks": ["#loginBtn", ".login-btn"]
  },
  "timestamp": 1727181
}
```

### Constraint 3 — JavaScript Popup Handling (Critical)
During **recording**, the engine must capture: dialog type, message, and user action.

During **code generation**, proper Playwright dialog handlers must be emitted **before** the triggering action:

```javascript
page.on('dialog', async dialog => {
  if (dialog.type() === 'confirm') {
    await dialog.accept();
  }
});
```

### Constraint 4 — Selector Strategy (Priority Order)
Selectors must be generated in this exact priority:
1. `data-testid`
2. `getByRole()`
3. `aria-label`
4. `placeholder`
5. CSS selectors
6. XPath — only as last resort

Requirements: avoid brittle selectors, avoid absolute XPath, implement fallback selector healing, retry failed selectors automatically.

### Constraint 5 — Generated Code Quality
Generated Playwright tests must:
- Use `@playwright/test` with `async/await`
- Include proper assertions
- Use auto-waiting (NO `waitForTimeout()`)
- Produce no noisy recorder artifacts, no duplicate locators
- Look professional and human-written

Example of acceptable output style:

```javascript
import { test, expect } from '@playwright/test';

test('Login flow', async ({ page }) => {
  await page.goto('https://example.com');
  await page.getByLabel('Username').fill('admin');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.getByText('Dashboard')).toBeVisible();
});
```

### Constraint 6 — UI/UX Requirements
- Dark theme with glassmorphism design
- Color scheme: Background `#0f172a`, Accent `#6366f1`, Success `#22c55e`, Error `#ef4444`
- Fully responsive (mobile + desktop)
- Pulsing recording indicator, animated logs, smooth transitions
- Monaco editor for code preview with syntax highlighting
- Copy-to-clipboard and `.spec.js` download button

### Constraint 7 — Project Setup Must Support
```bash
npm install
npm install --prefix backend
npm install --prefix frontend
npx --prefix backend playwright install chromium
```

With `package.json` scripts for: `setup`, `dev`, `start`, `build`.

---

## Folder Structure Required

```
/recorder-tool
  /frontend
  /backend
  /recorder
  /generator
  /playback
  /shared
```

---

## Output Requirements

Generate ALL of the following:
1. Complete frontend code
2. Complete backend code
3. Tailwind styling
4. API routes
5. Recorder engine
6. Playwright generator
7. Playback engine
8. `README.md`
9. Installation instructions
10. Example generated test
11. Folder structure

---

## Hard Constraints (DO NOT Violate)

- ❌ No brittle selectors
- ❌ No unnecessary XPath
- ❌ No `waitForTimeout()`
- ❌ No pseudo-code or skipped modules
- ❌ No noisy recorder artifacts
- ✅ Clean, executable, production-ready output only
