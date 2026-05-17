#!/bin/bash
# =============================================================
#  k29photo — setup.sh
#  Usage: bash setup.sh
#  Sets up the PostgreSQL database and starts the Flask portal.
# =============================================================

set -e  # Exit immediately on any error

# ------------------------------------------------------------
# Configuration — change these if needed
# ------------------------------------------------------------
DB_NAME="k29photo"
DB_USER="adamshawky"
FLASK_PORT=5000

echo "============================================="
echo "  k29photo Portal — Setup Script"
echo "============================================="

# ------------------------------------------------------------
# 1. Check dependencies
# ------------------------------------------------------------
echo ""
echo "[1/5] Checking dependencies..."

command -v psql    >/dev/null 2>&1 || { echo "ERROR: psql not found. Install PostgreSQL."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found."; exit 1; }
command -v pip3    >/dev/null 2>&1 || { echo "ERROR: pip3 not found."; exit 1; }

echo "      OK: psql, python3, pip3 found."

# ------------------------------------------------------------
# 2. Install Python dependencies
# ------------------------------------------------------------
echo ""
echo "[2/5] Installing Python dependencies..."
pip3 install -r requirements.txt --quiet
echo "      OK: dependencies installed."

# ------------------------------------------------------------
# 3. Create the database (drop if exists for clean setup)
# ------------------------------------------------------------
echo ""
echo "[3/5] Setting up database '$DB_NAME'..."

# Drop existing DB if present (clean slate)
psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS $DB_NAME;" postgres
psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"          postgres
echo "      OK: database created."

# ------------------------------------------------------------
# 4. Load schema and sample data
# ------------------------------------------------------------
echo ""
echo "[4/5] Loading schema and sample data..."

psql -U "$DB_USER" -d "$DB_NAME" -f schema.sql
echo "      OK: schema loaded."

psql -U "$DB_USER" -d "$DB_NAME" -f data.sql
echo "      OK: sample data loaded."

# Quick sanity check
echo ""
echo "      --- Data summary ---"
psql -U "$DB_USER" -d "$DB_NAME" -c \
  "SELECT
     (SELECT COUNT(*) FROM users)    AS users,
     (SELECT COUNT(*) FROM albums)   AS albums,
     (SELECT COUNT(*) FROM photos)   AS photos,
     (SELECT COUNT(*) FROM tags)     AS tags,
     (SELECT COUNT(*) FROM comments) AS comments,
     (SELECT COUNT(*) FROM likes)    AS likes;"

# ------------------------------------------------------------
# 5. Start the Flask portal
# ------------------------------------------------------------
echo ""
echo "[5/5] Starting k29photo portal on http://localhost:$FLASK_PORT"
echo "      Press Ctrl+C to stop."
echo "============================================="
echo ""

export FLASK_APP=app.py
export FLASK_ENV=development

python3 app.py