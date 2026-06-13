"""
Hafif şema göçü (lightweight migration).

`Base.metadata.create_all` yalnızca eksik TABLOLARI oluşturur; var olan bir
tabloya yeni KOLON eklemez. Alembic henüz kurulu olmadığından, mevcut
veritabanlarında eksik kolonları idempotent `ALTER TABLE ... IF NOT EXISTS`
ile ekliyoruz. Her açılışta güvenle çalışır; yeni DB'de no-op'tur.
"""
from sqlalchemy import text


# (tablo, kolon, kolon_tanımı) — Postgres ADD COLUMN IF NOT EXISTS destekler
_COLUMN_MIGRATIONS = [
    ("users", "is_admin", "BOOLEAN NOT NULL DEFAULT FALSE"),
    ("applications", "payment_status", "VARCHAR(20) NOT NULL DEFAULT 'unpaid'"),
    ("payments", "currency", "VARCHAR(8) NOT NULL DEFAULT 'TRY'"),
    ("payments", "plan", "VARCHAR(50)"),
    ("payments", "provider", "VARCHAR(20)"),
    ("payments", "provider_reference", "VARCHAR(255)"),
    ("payments", "paid_at", "TIMESTAMPTZ"),
]


async def run_lightweight_migrations(conn) -> None:
    """`engine.begin()` bloğu içinde, create_all'dan sonra çağrılır."""
    for table, column, ddl in _COLUMN_MIGRATIONS:
        await conn.execute(
            text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {ddl}')
        )
