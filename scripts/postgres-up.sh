#!/usr/bin/env bash
# Start local Postgres for lesson 12 (Homebrew postgresql@16).
set -euo pipefail

export PATH="/opt/homebrew/opt/postgresql@16/bin:/usr/local/opt/postgresql@16/bin:$PATH"

if ! command -v psql >/dev/null 2>&1; then
  echo "psql not found. Install: brew install postgresql@16"
  exit 1
fi

brew services start postgresql@16 >/dev/null 2>&1 || true

# wait until ready
for _ in $(seq 1 30); do
  if pg_isready -h 127.0.0.1 -p 5432 >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

if ! pg_isready -h 127.0.0.1 -p 5432 >/dev/null 2>&1; then
  echo "Postgres not ready on 127.0.0.1:5432"
  exit 1
fi

# role + db (idempotent)
psql -h 127.0.0.1 -d postgres -v ON_ERROR_STOP=1 <<'SQL' >/dev/null
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ship') THEN
    CREATE ROLE ship LOGIN PASSWORD 'ship';
  END IF;
END
$$;
SELECT 'ok' WHERE EXISTS (SELECT FROM pg_database WHERE datname = 'ship_ai');
SQL

if ! psql -h 127.0.0.1 -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='ship_ai'" | grep -q 1; then
  psql -h 127.0.0.1 -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE ship_ai OWNER ship;"
fi
psql -h 127.0.0.1 -d ship_ai -v ON_ERROR_STOP=1 -c "GRANT ALL ON SCHEMA public TO ship;" >/dev/null

echo "Postgres ready"
echo "DATABASE_URL=postgresql://ship:ship@127.0.0.1:5432/ship_ai"
echo "Smoke: npm run check:12"
