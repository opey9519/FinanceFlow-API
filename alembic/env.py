from urllib.parse import quote
from app.config import settings
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Alembic config object
config = context.config
fileConfig(config.config_file_name)

# Safely quote password
quoted_pass = quote(settings.POSTGRES_PASSWORD)
database_url = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{quoted_pass}@db:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Configure Alembic context **directly** (bypassing ConfigParser interpolation)


def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": database_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=settings.Base.metadata)
        with context.begin_transaction():
            context.run_migrations()
