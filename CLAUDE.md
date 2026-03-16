# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
python main.py
```

## Building the Executable

```bash
pyinstaller main.spec
```
Output: `dist/main.exe` (single executable with embedded icon)

## Architecture

This is a **multi-protocol industrial communication GUI** built with PySide6. It manages TCP/UDP/WebSocket/Bluetooth/HTTP/PLC connections and routes messages between them.

### Data Flow

```
User Action (GUI)
  → src/init.py (InitClass / QMainWindow)
  → src/protocols/SendHandler.py (message dispatcher)
  → Protocol threads (TCP/UDP/WebSocket/Bluetooth/HTTP/PLC)
  → Incoming messages → Message codec (src/protocols/msg/)
  → Controller (src/controller/) for business logic
  → Response via SendHandler
```

### Key Layers

**UI Layer** (`src/init.py`, `src/component/`): Main window with tabs for active servers, clients, PLC connections, and logs. Each subsystem has its own popup window (`Settings`, `PlcSettings`, `Handler`, `Utility`, `Direct`, `SqlHandler`).

**Protocol Layer** (`src/protocols/`): Each protocol has server/client thread pairs. Supported: TCP, UDP, WebSocket, Bluetooth, HTTP, and LS Electric PLC (via `snap7.dll`). Message codecs in `src/protocols/msg/`: `FreeCodec`, `JSONCodec`, `LengthCodec`.

**Controller Layer** (`src/controller/`): Business logic handlers invoked per message type. Add new controllers here for custom message processing. Active controller instances live in `conf/skModule.py`.

**Threading** (`src/thread/`): `WorkThread` refreshes connection lists in the UI; `LogThread` displays logs; `MsgHandler` handles message search/send from the main window.

**Persistence**: SQLite (`core.db`) stores socket configurations, message definitions, and handler mappings. Optional Tibero external DB via pyodbc (configured in `config.json`).

**Global State** (`conf/skModule.py`): Shared module-level data — active connection lists, combo box items, controller instances, and DB query lists used across the application.

### Configuration

- `config.json` (project root or `src/`): Database credentials for optional Tibero DB. Contains `USE_YN` flag to enable/disable external DB.
- `core.db`: SQLite database auto-created at runtime; stores all socket/handler/message configuration.
- `.ui` files: Qt Designer layouts at project root and `src/`. Compiled representations are in `ui/`.

### PLC Support

LS Electric PLC communication uses `snap7.dll` (must be present in the working directory). Thread implementation: `src/protocols/plc/PlcLsThread.py`. PLC settings UI: `src/component/plcSettings/`.

### Adding a New Message Controller

1. Create a class in `src/controller/` implementing the required handler method.
2. Register the instance in `conf/skModule.py`.
3. Map it to a message type in the Settings UI (`src/component/settings/Settings.py`).
