# Mini-Helpdesk-Mobiletic

A full-featured helpdesk application with a Laravel backend API and Angular frontend, running in Docker Compose for easy local development.

## Features

- Laravel 10.x backend (REST API, Sanctum auth, Eloquent, policies, validation)
- Angular 16+ frontend (planned)
- MySQL 8 database
- Docker Compose for orchestration
- Full API test coverage (feature & unit tests)
- Rich demo data: users, FAQs, tickets, comments

## Quick Start (Docker Compose)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with WSL2 for Windows)
- [Node.js 18+](https://nodejs.org/) (for frontend dev outside Docker)

git clone https://github.com/marouanbouchettoy/Mini-Helpdesk-Mobiletic.git
cd Mini-Helpdesk-Mobiletic
### 1. Clone the repository

```sh
git clone https://github.com/marouanbouchettoy/Mini-Helpdesk-Mobiletic.git
cd Mini-Helpdesk-Mobiletic
```

docker-compose up --build
### 2. Start all services

```sh
docker-compose up --build
```

- Backend API: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:4200](http://localhost:4200)
- MySQL: localhost:3307 (user: helpdesk, pass: helpdesk123)

### 3. First run (backend)

- Installs Composer deps, runs migrations & seeds, generates .env, and starts API server automatically.
- Demo users: see `backend/database/seeders/DatabaseSeeder.php` for emails/passwords.

docker-compose exec backend php artisan test
### 4. Running tests

```sh
docker-compose exec backend php artisan test
```

### 5. Useful commands

- Rebuild containers: `docker-compose up --build`
- Reseed DB: `docker-compose exec backend php artisan migrate:fresh --seed --force`
- Artisan: `docker-compose exec backend php artisan <command>`
- NPM (frontend): `docker-compose exec frontend npm <command>`

## Environment Variables

- See `backend/.env.example` for backend config (copied to `.env` on first run)
- DB defaults: host `mysql`, user `helpdesk`, pass `helpdesk123`, db `helpdesk`

## Folder Structure

- `backend/` — Laravel API
- `frontend/` — Angular app
- `docker-compose.yml` — Orchestration

## Production

For production, adjust `.env` and Docker Compose for secure passwords, disable debug, and use production builds.

## License

MIT
