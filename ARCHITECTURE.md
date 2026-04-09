# System Architecture

## Overview
AccessiAI is composed of a decoupled Frontend and Backend, orchestrated via Docker Containerization. The stack leverages React for rapid UI updates, Django for backend REST processing, and PyTorch (HuggingFace) and spaCy for native AI integrations.

## Tech Stack
*   **Frontend**: React + Vite (Port 5173)
*   **Backend**: Django + Django REST Framework + Channels (Port 8000)
*   **Database**: PostgreSQL
*   **AI/CV Module**: `transformers` ViT-GPT2 for image captioning.
*   **AI/NLP Module**: `spaCy` for text/layout simplification.

## Data Flow (Accessibility Scan)

1. **Client Request**: The User enters a URL into the Dashboard (`React`).
2. **REST Invocation**: An `Axios`/`Fetch` POST request is fired to the Django endpoint `POST /api/scanner/scan/`.
3. **Data Scrubbing**: `BeautifulSoup4` extracts the DOM layout, scraping for standard WCAG accessibility violations (Missing `alt` tags, bad heading hierarchies).
4. **AI Generation Pipeline (Parallel)**:
   *   Images without `alt` text are asynchronously pushed to the ViT-GPT2 endpoint (`ai_vision.py`), generating localized text-descriptions from the pixel data.
   *   Cluttered text nodes are pushed to `nlp_simplifier.py` which isolates semantic subjects from non-semantic visual noise.
5. **Database Transaction**: The combined accessibility score and AI payloads are written to the default PostgreSQL `ScanResult` table.
6. **Client Render**: A JSON payload returns to React, dynamically filling out the dashboard and enabling the User to toggle the Native View vs. the Simplified Layout.

## Real-time Interactions (WebSockets)
To assist users dynamically, the platform supports real-time text-to-speech. 
*   Django `Channels` opens an asynchronous `WebSocket` stream (`ws://localhost:8000/ws/`).
*   Instead of waiting for an entire TTS audio file to render linearly (which requires massive blocking HTTP buffers), chunks of generated vocal audio stream directly to the client as they become generated.
