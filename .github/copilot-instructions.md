# EventWorld AI Coding Guidelines

## Architecture Overview
EventWorld is a Django REST API backend with Vue 3 frontend, designed for event management and ticketing. Key components:
- **Backend**: Django 5.1 + DRF with JWT authentication, custom user roles (organisateur/association/étudiant/autre)
- **Frontend**: Vue 3 + Vite + Capacitor mobile app with QR scanning capabilities
- **Database**: PostgreSQL (Docker) / SQLite (local dev)
- **Key Models**: User (custom roles), Evenement (events with JSON price_categories), TemporaryScanner (event staff), Ticketing (QR tickets)

## Critical Patterns & Conventions

### User Roles & Permissions
- Role-based event creation: `user.can_create_event(event_type)` in `models.py`
- Organisateurs/Associations: all event types; Étudiants: private/limited; Autres: private only
- Custom permission classes: `IsOrganizerOrAssociation` in `permissions.py`
- Temporary scanners have time-limited access tokens with granular permissions (can_scan, can_sell)

### Event Management
- Events use JSON `price_categories` field: `{"standard": 10.0, "vip": 25.0}`
- Auto-generated `code_evenement` (8-char UUID) on save
- Picture uploads to `event_pictures/` with auto-deletion of old images via `pre_save` signal
- Status workflow: draft → current → finished/cancelled

### API Design
- DRF ModelViewSets with custom `get_queryset()` filtering by user role
- JWT tokens: 1-day access, 7-day refresh with rotation/blacklist
- CORS configured for localhost:5173 (frontend dev server)
- Custom middleware: `TemporaryScannerEventRestrictionMiddleware`

### Temporary Scanners
- UUID access tokens for secure login
- Online status: last_seen within 5 minutes
- KPI tracking: tickets_scanned, tickets_sold
- Expiration handling with `is_active()` method

### Ticketing System
- UUID QR codes for security
- Status: valid/used/invalid with scan timestamps
- Supports bulk purchases (quantity field)
- Buyer info stored: firstname/lastname/email/phone

## Development Workflows

### Local Development
```bash
# Backend + Frontend servers
./start_serveurs.bat  # Windows: starts both servers in background

# Or manually:
python manage.py runserver  # Backend on :8000
cd frontend/frontendEventWorld && npm run dev  # Frontend on :5173
```

### Docker Development
```bash
docker-compose up --build  # Full stack with Postgres
# Backend waits 10s for DB, runs migrations automatically
```

### Database Setup
- Local: PostgreSQL with credentials in `.env.local`
- Docker: Postgres container with volume persistence
- Migrations: `python manage.py makemigrations && python manage.py migrate`

### Testing
- Frontend: Vitest unit tests, Cypress E2E
- Backend: Django test framework (minimal test files in `tests/`)

### CI/CD
- Jenkins pipeline: Docker Compose deployment
- GitLab integration (project originally from GitLab)

## Key Files & Directories
- `EventWorldApp/models.py`: Core data models with business logic
- `EventWorldApp/views/`: API endpoints (EventView, Ticketing, ScanView, etc.)
- `EventWorldApp/utils/serializers.py`: DRF serializers
- `frontend/frontendEventWorld/src/`: Vue components, Pinia stores, QR scanning
- `docker-compose.yml`: Multi-service setup (backend/frontend/db)
- `.env.local`/`.env.docker`: Environment-specific config

## Common Gotchas
- Environment detection: `ENVIRONMENT` env var switches between `.env.local` and `.env.docker`
- User role validation happens in model `save()` methods, not just views
- Temporary scanner tokens expire but aren't auto-cleaned; check `is_active()`
- Event pictures: old files deleted via signal, but path handling assumes media root
- CORS: `CORS_ORIGIN_ALLOW_ALL=True` for dev, but specific origins commented out

## Mobile App Features
- Capacitor for iOS/Android builds
- QR code generation/scanning with `vue-qrcode-reader`
- Offline-capable ticket scanning
- PDF generation with jsPDF for tickets</content>
<parameter name="filePath">d:\Projets\Eventworld\eventworld\.github\copilot-instructions.md