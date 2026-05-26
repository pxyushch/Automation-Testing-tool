# AutoTest Recorder

Production-grade AI-powered Record & Playback Automation Platform.

## Setup

```bash
npm run setup
npm run dev
```

## Production

```bash
npm run setup
npm run build
npm start
```

The backend serves the compiled frontend and exposes a health endpoint at
`/api/health`.

## Deploy on Render

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint**.
3. Select the GitHub repository.
4. Render will read `render.yaml`, build the frontend, and start the Express
   server.
