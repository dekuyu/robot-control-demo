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
        │       ├── EmergencyStop.vue    ✅ DONE
        │       ├── AlarmBanner.vue      ✅ DONE
        │       ├── StatusIndicator.vue   ✅ DONE
        │       ├── SpeedSlider.vue       ✅ DONE
        │       ├── ConfirmDialog.vue     ✅ DONE
        │       ├── AxisSlider.vue       ✅ DONE
        │       ├── UdpTerminal.vue       ✅ DONE
        │       ├── JointAngleDisplay.vue ✅ DONE
        │       ├── EndCoordDisplay.vue   ✅ DONE
        │       ├── TorqueDisplay.vue     ✅ DONE
        │       ├── RobotStatusPanel.vue  ✅ DONE
        │       ├── PermissionGuard.vue   ✅ DONE
        │       ├── VariableEditor.vue    ✅ DONE
        │       ├── IOMatrix.vue          ✅ DONE
        │       ├── PositionCard.vue      ✅ DONE
        │       ├── LogTable.vue          ✅ DONE
        │       ├── SafetyBanner.vue      ✅ DONE
        │       ├── CoordInput.vue        ✅ DONE
        │       └── NotificationToast.vue ✅ DONE
        │
        └── views/                  # Page views
            ├── LoginView.vue        ✅ DONE
            ├── DashboardView.vue    ✅ DONE
            ├── ControlView.vue      ✅ DONE
            ├── PositionView.vue     ✅ DONE
            ├── VariableView.vue     ✅ DONE
            ├── AlarmView.vue        ✅ DONE
            ├── LogView.vue          ✅ DONE
            ├── SafetyView.vue       ✅ DONE
            ├── SettingsView.vue     ✅ DONE
            ├── AdminView.vue         ✅ DONE
            └── TerminalView.vue     ✅ DONE
```

## Progress Summary

### ✅ Completed (Backend 100% + Frontend 100%)

**Backend** - All files complete:
- Infrastructure: config, database, dependencies, core modules (security, exceptions, middleware, error_codes, constants)
- Utils: encoding, validators, time_utils, logging_utils
- Models: 8 ORM models with PostgreSQL tables
- Schemas: 12 Pydantic schema modules
- Services: 12 service modules including YERC protocol, UDP client, all business logic
- API Routes: 11 route modules covering all REST endpoints
- Tasks: Background polling tasks (status, position, torque, alarm, heartbeat)
- Entry: main.py with CORS, exception handlers, health checks

**Frontend** - All files complete:
- Build config: package.json, vite.config.ts, tsconfig
- Styles: 4 SCSS files with industrial dark theme
- Types: 10 TypeScript type definition modules
- Utils: 6 utility modules
- Stores: **10** Pinia stores (auth, robot, connection, control, alarm, safety, position, variable, log, user)
- API Services: **11** API modules with Axios client (including alarm.ts)
- WebSocket: connection.ts + messageHandler.ts
- Composables: 5 composable functions
- Router: Full route definitions with auth guards
- Layouts: MainLayout + AuthLayout
- Components: **19** Vue components (StatusIndicator, AlarmBanner, EmergencyStop, SpeedSlider, ConfirmDialog, NotificationToast, PermissionGuard, JointAngleDisplay, EndCoordDisplay, TorqueDisplay, RobotStatusPanel, AxisSlider, CoordInput, PositionCard, LogTable, VariableEditor, IOMatrix, SafetyBanner, UdpTerminal)
- Views: **11** pages (Login, Dashboard, Control, Position, Variable, Alarm, Log, Safety, Settings, Admin, Terminal)
- Entry: main.ts, App.vue
