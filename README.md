# 🎥 Video Frame Extractor

## 🛠️ Description
A deterministic frame preprocessing engine that injects the overlay object on top of the video frames.

### 🔄 Execution Pipeline Architecture

```text
[ Background video ] + [ Overlay object ] + [ Config ]
        │
        ▼
[ Ingestion & Validation ] ──► [ State Container ]
                                      │
                                      ▼
                          [ Frame Extraction ]
                                      │
                                      ▼
                          [ Overlay Application ]
                                      │
                                      ▼
                          [ State Container ]
                                      │
                                      ▼
                          [ JSON Output ] ──► [ Frames Package (.zip) ]
```

### 📚 Resources & Documentation
- **Tutorial/Book:** ***currently in development***

---

### 🧮 Performance Audit:
### Audit: 2026-08-25 00:14:01 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32792613342)
- **CPU Load:** `31.7%`
- **Memory Usage:** `125/15992MB`
### Audit: 2026-08-24 23:37:00 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32789944562)
- **CPU Load:** `32.5%`
- **Memory Usage:** `124/15988MB`
### Audit: 2026-08-24 23:24:15 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32788977663)
- **CPU Load:** `32.6%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 23:10:36 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32788077683)
- **CPU Load:** `2.4%`
- **Memory Usage:** `1054/15988MB`
### Audit: 2026-08-24 22:25:33 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32784437714)
- **CPU Load:** `34.1%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 16:01:37 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32748005116)
- **CPU Load:** `38.1%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 15:44:34 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32746307448)
- **CPU Load:** `33.4%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 15:30:11 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32744886967)
- **CPU Load:** `34.9%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 15:09:49 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32742810990)
- **CPU Load:** `39.5%`
- **Memory Usage:** `124/15993MB`
### Audit: 2026-08-24 15:03:39 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32742195992)
- **CPU Load:** `33.4%`
- **Memory Usage:** `124/15993MB`
### Audit: 2026-08-24 14:54:04 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32741154144)
- **CPU Load:** `35.7%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 14:28:29 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32738555718)
- **CPU Load:** `39%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 14:08:01 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32736442754)
- **CPU Load:** `31.7%`
- **Memory Usage:** `124/15988MB`
### Audit: 2026-08-24 14:00:41 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32735551632)
- **CPU Load:** `38.1%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 13:33:56 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32733060239)
- **CPU Load:** `42.9%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 13:28:45 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32732589792)
- **CPU Load:** `43.9%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 13:18:37 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32731587698)
- **CPU Load:** `40.5%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 13:12:19 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32730995772)
- **CPU Load:** `34.1%`
- **Memory Usage:** `124/15988MB`
### Audit: 2026-08-24 12:54:25 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32729288811)
- **CPU Load:** `47.6%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 12:20:54 UTC
- **Branch:** `main`
- **Status:** `failure`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32726516938)
- **CPU Load:** `32.6%`
- **Memory Usage:** `124/15989MB`
### Audit: 2026-08-24 12:15:35 UTC
- **Branch:** `main`
- **Status:** `success`
- **Run:** [Detailed Execution Logs](https://github.com/Dmitrii-Zavalin-Deployments/video_frame_extractor/actions/runs/32726077340)
- **CPU Load:** `38.1%`
- **Memory Usage:** `124/15989MB`
