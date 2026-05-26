# Prompt: AI-Powered Record & Playback Automation Tool

Act as a senior full-stack engineer and UI/UX architect building a production grade AI powered Record & Playback Automation Tool.

The goal is to create a modern web application that records browser interactions and automatically generates clean, executable Playwright test scripts.

The final product should be a real SaaS-quality automation platform:
- Modern
- Responsive
- Smooth
- Reliable
- Maintainable
- Production-ready

PROJECT OVERVIEW

Build a Record & Playback Tool with:
1. Browser interaction recording
2. Playwright code generation
3. Playback execution
4. Modern responsive UI
5. JavaScript popup handling
6. Smart selector strategy
7. Clean exportable test scripts

TECH STACK

Frontend:
- React
- Tailwind CSS
- Framer Motion for animations

Backend:
- Node.js
- Express.js

Automation:
- Playwright

Optional:
- WebSocket for live logs
- Monaco editor for code preview

ARCHITECTURE PLANNING

Before writing code:
1. Define complete architecture
2. Break system into modules:
   - Frontend UI
   - Recorder Engine
   - Event Processor
   - Playwright Code Generator
   - Playback Engine
   - Export Manager
3. Explain data flow:
   - Record → Process → Store → Generate → Playback
4. Define folder structure
5. Define API routes
6. Explain how popup handling and selector healing will work

RECORDING ENGINE

Build a recording engine that captures:
- Clicks
- Inputs
- Dropdown selections
- Checkbox interactions
- Navigation events
- Page transitions
- Keyboard actions
- JavaScript dialogs:
  - alert
  - confirm
  - prompt

Store all actions in structured JSON format.

Example:

{
  "type": "click",
  "selector": {
    "primary": "getByRole(button)",
    "fallbacks": ["#loginBtn", ".login-btn"]
  },
  "timestamp": 1727181
}

JAVASCRIPT POPUP HANDLING (CRITICAL)

The tool MUST properly handle:
- alert()
- confirm()
- prompt()

During recording:
- Capture:
  - dialog type
  - dialog message
  - user action
  - prompt input text

During code generation:
Generate proper Playwright dialog handlers BEFORE triggering actions.

Example:

page.on('dialog', async dialog => {
  if (dialog.type() === 'confirm') {
    await dialog.accept();
  }
});

For prompt:

page.on('dialog', async dialog => {
  if (dialog.type() === 'prompt') {
    await dialog.accept('sample input');
  }
});

SELECTOR STRATEGY (VERY IMPORTANT)

Implement reliable selector generation.

Priority order:
1. data-testid
2. getByRole()
3. aria-label
4. placeholder
5. CSS selectors
6. XPath only as fallback

Requirements:
- Avoid brittle selectors
- Avoid absolute XPath
- Implement fallback selector healing
- Retry failed selectors automatically

PLAYWRIGHT CODE GENERATOR

Generate clean production-ready Playwright tests using:
- @playwright/test
- async/await
- proper assertions
- auto-waiting

Requirements:
- No waitForTimeout()
- No noisy recorder artifacts
- No duplicate locators
- Remove unnecessary clicks
- Generate readable code

Generated code should look professional and human-written.

Example style:

import { test, expect } from '@playwright/test';

test('Login flow', async ({ page }) => {
  await page.goto('https://example.com');

  await page.getByLabel('Username').fill('admin');
  await page.getByLabel('Password').fill('password');

  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page.getByText('Dashboard')).toBeVisible();
});

PLAYBACK ENGINE

Build playback functionality that:
- Replays recorded actions
- Highlights active elements
- Shows real-time execution logs
- Handles popup dialogs
- Supports retries
- Shows success/failure states

MODERN UI/UX

Build a trendy modern UI.

Design Style:
- Dark theme
- Glassmorphism
- Minimal and clean
- Premium SaaS feel

Primary colors:
- Background: #0f172a
- Accent: #6366f1
- Success: #22c55e
- Error: #ef4444

UI LAYOUT

Top Navbar:
- App logo/title: “AutoTest Recorder”
- Recording status indicator
- Start / Stop / Playback buttons

Left Sidebar:
- Saved sessions
- Recording history
- Settings

Main Workspace:
1. URL input section
2. Live recording logs
3. Playback logs
4. Code preview panel
5. Export/download button

UI FEATURES

Requirements:
- Fully responsive
- Mobile + desktop support
- Smooth animations
- Fast transitions
- Loading states
- Skeleton loaders
- Hover effects
- Syntax highlighted code editor
- Copy-to-clipboard
- Download .spec.js button

MICRO-INTERACTIONS

Add:
- Pulsing recording indicator
- Smooth hover glow
- Animated logs
- Button loading animations
- Smooth page transitions

CODE QUALITY

Requirements:
- Modular architecture
- Reusable components
- Proper error handling
- Retry mechanisms
- Logging system
- Clean code practices
- Comments where necessary
- Type-safe architecture if possible

ADVANCED FEATURES

Support:
- iFrames
- Shadow DOM
- Dynamic content
- Lazy loading
- Multiple tabs
- Screenshot on failure
- Session persistence

ERROR HANDLING & INPUT VALIDATION (MANDATORY)

The entire platform must implement enterprise-grade error handling, validation, resilience, and recovery mechanisms across frontend, backend, recorder engine, playback engine, and Playwright generation.

The system must NEVER silently fail.

All errors must be:
- Captured
- Logged
- Displayed clearly
- Recoverable when possible

FRONTEND VALIDATION

Validate all user inputs before sending requests.

URL Validation:
Validate:
- Proper protocol (http:// or https://)
- Invalid domains
- Empty URLs
- Unsupported browser URLs

Show user-friendly validation messages.

Examples:
- “Please enter a valid URL”
- “Unsupported protocol detected”
- “URL is unreachable”

Prevent invalid submissions.

Form Validation:
Validate:
- Required fields
- Empty inputs
- Invalid settings
- Playback configuration values
- Export names
- Timeout values

Use:
- Inline validation
- Error tooltips
- Disabled submit buttons when invalid

UI Error States:
Implement:
- Error boundaries in React
- Global toast notifications
- Retry actions
- Fallback UI
- Empty states
- Network error screens
- Offline detection

Examples:
- “Playback failed”
- “Recorder disconnected”
- “Unable to generate Playwright script”

BACKEND ERROR HANDLING

All API routes must implement:

Request Validation:
Use:
- Zod
OR
- Joi
OR
- express-validator

Validate:
- Request body
- Query params
- Headers
- Payload schema

Reject malformed requests with proper HTTP codes.

Example status codes:
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Validation Error
- 500 Internal Server Error

Global Error Middleware:
Implement centralized Express error handling middleware.

Requirements:
- Structured JSON errors
- Stack traces only in development
- Sanitized production errors
- Request correlation IDs
- Timestamped logs

Example response:

{
  "success": false,
  "error": {
    "message": "Invalid playback session",
    "code": "PLAYBACK_SESSION_INVALID",
    "timestamp": "2026-01-01T10:00:00Z"
  }
}

Logging System:
Implement structured logging using:
- Winston
OR
- Pino

Log:
- API failures
- Playback failures
- Selector failures
- Dialog handling failures
- Browser crashes
- Timeout issues
- Export failures

Support:
- Console logging
- File logging
- Error log separation

RECORDER ENGINE ERROR HANDLING

The recorder engine must safely handle:
- Detached DOM nodes
- Dynamic page updates
- Cross-origin iframe restrictions
- Missing selectors
- Stale elements
- Browser crashes
- Page reloads
- Navigation interruptions

Requirements:
- Auto-recovery
- Graceful degradation
- Event buffering
- Event deduplication
- Retry failed recordings
- Prevent duplicate event injection

If recording fails:
- Preserve partial session state
- Notify the user
- Allow recovery/restart

PLAYBACK ENGINE RESILIENCE

Playback engine must include:

Retry Mechanisms:
Implement configurable retries for:
- Missing selectors
- Delayed rendering
- Network instability
- Lazy-loaded elements
- Dialog timing issues

Requirements:
- Exponential backoff
- Smart retry logic
- Max retry limits

Selector Healing:
If a selector fails:
1. Try fallback selectors
2. Re-evaluate semantic selectors
3. Retry with alternative strategies
4. Log selector recovery attempts

Never fail immediately on first selector miss.

Playback Failure Handling:
On playback failure:
- Capture screenshot
- Save HTML snapshot
- Save execution logs
- Highlight failed step
- Generate readable error report

Include:
- Failed selector
- Timeout reason
- Last successful action
- DOM snapshot reference

PLAYWRIGHT GENERATOR VALIDATION

Generated scripts must be validated before export.

Requirements:
- Remove duplicate actions
- Remove invalid selectors
- Validate generated syntax
- Ensure imports exist
- Ensure async flow correctness
- Prevent unreachable code

Generated code must:
- Pass ESLint formatting
- Avoid dead code
- Avoid redundant awaits
- Avoid invalid Playwright APIs

WEBSOCKET ERROR HANDLING

If WebSocket is used:

Implement:
- Auto reconnect
- Heartbeat/ping mechanism
- Connection timeout handling
- Reconnection status UI
- Graceful fallback to polling

Handle:
- Lost connections
- Partial messages
- Invalid payloads

SECURITY VALIDATION

Implement:
- Rate limiting
- Helmet.js security headers
- CORS configuration
- Payload size limits
- Input sanitization
- XSS prevention
- CSRF protection where needed

Never execute unsafe user-generated scripts.

FILE EXPORT VALIDATION

Before exporting:
- Validate generated test integrity
- Prevent empty exports
- Validate file names
- Ensure UTF-8 encoding

Support:
- Safe download handling
- Export failure recovery

PERFORMANCE SAFEGUARDS

Implement safeguards for:
- Large recording sessions
- Memory leaks
- Infinite event loops
- Excessive DOM mutations
- High-frequency event spam

Requirements:
- Event throttling
- Debouncing
- Cleanup listeners
- Session size limits

TIMEOUT MANAGEMENT

Implement configurable timeout handling for:
- Navigation
- Selector resolution
- Playback steps
- API requests
- Browser launch

Requirements:
- Sensible defaults
- Timeout override settings
- Timeout-specific error messages

OBSERVABILITY & DEBUGGING

Implement:
- Debug mode
- Verbose logging mode
- Session replay diagnostics
- Execution timeline
- Network request tracing
- Performance metrics

Support:
- Failure reproduction
- Exportable debug logs

FINAL QUALITY REQUIREMENTS

The final system must behave like a production SaaS application with:
- Graceful failures
- Self-healing mechanisms
- Reliable recovery flows
- Clear user feedback
- Stable automation execution
- Enterprise-level resilience

The application must prioritize:
1. Reliability
2. Stability
3. Maintainability
4. Fault tolerance
5. User experience
6. Automation accuracy

OUTPUT REQUIREMENTS

Generate:
1. Complete frontend code
2. Complete backend code
3. Tailwind styling
4. API routes
5. Recorder engine
6. Playwright generator
7. Playback engine
8. README.md
9. Installation instructions
10. Example generated test
11. Folder structure

FOLDER STRUCTURE
```
/recorder-tool
  /frontend
  /backend
  /recorder
  /generator
  /playback
  /shared
```
SETUP REQUIREMENTS

Project should support:
npm install
npm install --prefix backend
npm install --prefix frontend
npx --prefix backend playwright install chromium

Add package.json scripts for:
- setup
- dev
- start
- build

IMPORTANT CONSTRAINTS

DO NOT:
- Use brittle selectors
- Use unnecessary XPath
- Use waitForTimeout()
- Generate pseudo code
- Skip modules
- Create noisy recorder artifacts

ENSURE:
- Clean generated Playwright scripts
- Reliable automation
- Responsive UI
- Smooth UX
- Production-ready structure
- Real-world usability

FINAL GOAL

The final product should look and feel like a modern enterprise automation platform that could realistically compete with lightweight record-and-playback testing tools.
