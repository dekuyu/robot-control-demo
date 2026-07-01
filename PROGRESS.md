# YRC1000 Robot Control System - Project Structure

```
robot-control-demo/
├── 功能需求文档.md               # PRD document
├── 架构设计.md                     # Architecture design document
├── 设计要求.md                     # Design requirements document
│
├── backend/                       # Python FastAPI backend
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables
│   ├── alembic.ini                # Alembic config
│   ├── alembic/
│   │   ├── env.py                 # Alembic async env
│   │   └── versions/
│   │       └── 001_initial_tables.py
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py                # FastAPI entry point
│       ├── config.py              # Pydantic Settings
│       ├── database.py            # Async engine + session
│       ├── dependencies.py         # DI: get_db, get_current_user
│       │
│       ├── core/                   # Core infrastructure
│       │   ├── __init__.py
│       │   ├── security.py         # JWT + bcrypt
│       │   ├── exceptions.py       # Custom exceptions
│       │   ├── middleware.py       # CORS + logging
│       │   ├── error_codes.py     # Error code definitions
│       │   └── constants.py       # Global constants
│       │
│       ├── utils/                  # Utility functions
│       │   ├── __init__.py
│       │   ├── encoding.py         # YERC value encoding
│       │   ├── validators.py       # Input validation
│       │   ├── time_utils.py       # Time utilities
│       │   └── logging_utils.py    # Operation logging
│       │
│       ├── models/                 # SQLAlchemy ORM models
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── user.py
│       │   ├── robot_config.py
│       │   ├── operation_log.py
│       │   ├── alarm_history.py
│       │   ├── saved_position.py
│       │   ├── safety_config.py
│       │   └── packet_log.py
│       │
│       ├── schemas/               # Pydantic schemas
│       │   ├── __init__.py
│       │   ├── common.py
│       │   ├── user.py
│       │   ├── robot.py
│       │   ├── control.py
│       │   ├── safety.py
│       │   ├── position.py
│       │   ├── variable.py
│       │   ├── alarm.py
│       │   ├── log.py
│       │   ├── ws.py
│       │   └── terminal.py
│       │
│       ├── services/              # Business logic layer
│       │   ├── __init__.py
│       │   ├── yerc_protocol.py    # YERC protocol codec
│       │   ├── udp_client.py       # UDP client
│       │   ├── ws_manager.py       # WebSocket manager
│       │   ├── auth.py            # Auth service
│       │   ├── robot.py           # Robot connection
│       │   ├── safety.py          # Safety checks
│       │   ├── control.py         # Motion control
│       │   ├── position.py        # Position management
│       │   ├── variable.py        # Variable read/write
│       │   ├── alarm.py           # Alarm management
│       │   ├── log.py             # Operation logs
│       │   ├── user.py            # User management
│       │   └── terminal_service.py # Debug terminal
│       │
│       ├── api/                   # API routes
│       │   ├── __init__.py
│       │   ├── router.py          # Route aggregation
│       │   ├── auth.py            # /api/auth/*
│       │   ├── robot.py           # /api/robot/*
│       │   ├── safety.py          # /api/safety/*
│       │   ├── control.py         # /api/control/*
│       │   ├── position.py        # /api/positions/*
│       │   ├── variable.py        # /api/variables/*
│       │   ├── alarm.py           # /api/alarms/*
│       │   ├── log.py             # /api/logs/*
│       │   ├── user.py            # /api/users/*
│       │   ├── ws.py              # /ws WebSocket
│       │   └── terminal.py        # /api/terminal/*
│       │
│       └── tasks/                 # Background tasks
│           ├── __init__.py
│           └── background.py      # Polling tasks
│
└── frontend/                      # Vue3 + TypeScript frontend
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tsconfig.node.json
    ├── index.html
    ├── .env.development
    │
    └── src/
        ├── main.ts                 # App entry
        ├── App.vue                 # Root component
        ├── env.d.ts               # Type declarations
        │
        ├── styles/                 # SCSS styles
        │   ├── variables.scss      # Color/font/spacing vars
        │   ├── global.scss         # Reset + Element Plus dark
        │   ├── industrial.scss     # Industrial components
        │   └── mixins.scss         # SCSS mixins
        │
        ├── types/                  # TypeScript types
        │   ├── api.ts
        │   ├── user.ts
        │   ├── robot.ts
        │   ├── control.ts
        │   ├── alarm.ts
        │   ├── position.ts
        │   ├── variable.ts
        │   ├── log.ts
        │   ├── safety.ts
        │   └── ws.ts
        │
        ├── utils/                  # Utilities
        │   ├── constants.ts
        │   ├── format.ts
        │   ├── permission.ts
        │   ├── safety.ts
        │   ├── export.ts
        │   └── validators.ts
        │
        ├── stores/                 # Pinia stores
        │   ├── auth.ts
        │   ├── robot.ts
        │   ├── connection.ts
        │   ├── control.ts
        │   ├── alarm.ts
        │   └── safety.ts
        │
        ├── api/                    # HTTP API services
        │   ├── client.ts           # Axios instance
        │   ├── auth.ts
        │   ├── robot.ts
        │   ├── control.ts
        │   ├── safety.ts
        │   ├── position.ts
        │   ├── variable.ts
        │   ├── log.ts
        │   ├── user.ts
        │   └── terminal.ts
        │
        ├── ws/                     # WebSocket
        │   ├── connection.ts
        │   └── messageHandler.ts
        │
        ├── composables/            # Composable functions
        │   ├── useWebSocket.ts
        │   ├── useKeyboard.ts
        │   ├── usePermission.ts
        │   ├── useSafetyCheck.ts
        │   └── useJogControl.ts
        │
        ├── router/
        │   └── index.ts            # Vue Router
        │
        ├── layouts/
        │   ├── MainLayout.vue
        │   └── AuthLayout.vue
        │
        ├── components/
        │   └── common/
        │       ├── EmergencyStop.vue    ⏳ NOT YET
        │       ├── AlarmBanner.vue      ⏳ NOT YET
        │       ├── StatusIndicator.vue   ⏳ NOT YET
        │       ├── SpeedSlider.vue       ⏳ NOT YET
        │       ├── ConfirmDialog.vue     ⏳ NOT YET
        │       ├── AxisSlider.vue       ⏳ NOT YET
        │       ├── UdpTerminal.vue       ⏳ NOT YET
        │       └── ... (many more)       ⏳ NOT YET
        │
        └── views/                  # Page views
            ├── LoginView.vue        ⏳ NOT YET
            ├── DashboardView.vue    ⏳ NOT YET
            ├── ControlView.vue      ⏳ NOT YET
            ├── PositionView.vue     ⏳ NOT YET
            ├── VariableView.vue     ⏳ NOT YET
            ├── AlarmView.vue        ⏳ NOT YET
            ├── LogView.vue          ⏳ NOT YET
            ├── SafetyView.vue       ⏳ NOT YET
            ├── SettingsView.vue     ⏳ NOT YET
            ├── AdminView.vue         ⏳ NOT YET
            └── TerminalView.vue     ⏳ NOT YET
```

## Progress Summary

### ✅ Completed (Backend 100% + Frontend Core ~60%)

**Backend** - All files complete:
- Infrastructure: config, database, dependencies, core modules (security, exceptions, middleware, error_codes, constants)
- Utils: encoding, validators, time_utils, logging_utils
- Models: 8 ORM models with PostgreSQL tables
- Schemas: 12 Pydantic schema modules
- Services: 12 service modules including YERC protocol, UDP client, all business logic
- API Routes: 11 route modules covering all REST endpoints
- Tasks: Background polling tasks (status, position, torque, alarm, heartbeat)
- Entry: main.py with CORS, exception handlers, health checks

**Frontend** - Core infrastructure complete:
- Build config: package.json, vite.config.ts, tsconfig
- Styles: 4 SCSS files with industrial dark theme
- Types: 10 TypeScript type definition modules
- Utils: 6 utility modules
- Stores: 6 Pinia stores (auth, robot, connection, control, alarm, safety)
- API Services: 10 API modules with Axios client
- WebSocket: connection.ts + messageHandler.ts
- Composables: 5 composable functions
- Router: Full route definitions with auth guards
- Layouts: MainLayout + AuthLayout
- Entry: main.ts, App.vue

### ❌ Not Yet Created (Frontend Views + Components)

**Views** (11 pages):
1. `LoginView.vue` - Login page
2. `DashboardView.vue` - Dashboard/status overview
3. `ControlView.vue` - Robot arm control (servo, jog, axis, speed)
4. `PositionView.vue` - Position management
5. `VariableView.vue` - Variable read/write panel
6. `AlarmView.vue` - Alarm management
7. `LogView.vue` - Operation log viewer
8. `SafetyView.vue` - Safety configuration
9. `SettingsView.vue` - System settings
10. `AdminView.vue` - User management
11. `TerminalView.vue` - UDP debug terminal

**Components** (15+):
- EmergencyStop.vue, AlarmBanner.vue, StatusIndicator.vue
- SpeedSlider.vue, ConfirmDialog.vue, AxisSlider.vue
- UdpTerminal.vue, JointAngleDisplay.vue, EndCoordDisplay.vue
- TorqueDisplay.vue, RobotStatusPanel.vue, PermissionGuard.vue
- VariableEditor.vue, IOMatrix.vue, PositionCard.vue, LogTable.vue
- SafetyBanner.vue, CoordInput.vue, NotificationToast.vue

**Additional Stores**:
- position.ts, variable.ts, log.ts, user.ts (simpler stores)
