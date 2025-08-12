"""Alembic environment configuration for ERPNext AI System."""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import our models and configuration
from core.database import Base
from core.config import settings

# Import all model modules to ensure they're registered
from modules.accounts.customer import Customer
from modules.accounts.supplier import Supplier
from modules.accounts.account import Account
from modules.accounts.payment_entry import PaymentEntry
from modules.sales.sales_order import SalesOrder
from modules.sales.sales_invoice import SalesInvoice
from modules.sales.quotation import Quotation
from modules.purchase.purchase_order import PurchaseOrder
from modules.purchase.purchase_invoice import PurchaseInvoice
from modules.stock.item import Item
from modules.stock.warehouse import Warehouse
from modules.stock.stock_entry import StockEntry
from modules.hr.employee import Employee
from modules.hr.salary_structure import SalaryStructure
from modules.projects.project import Project
from modules.projects.task import Task
from modules.crm.lead import Lead
from modules.crm.opportunity import Opportunity
from modules.support.issue import Issue
from modules.manufacturing.bom import BOM
from modules.manufacturing.work_order import WorkOrder
from modules.assets.asset import Asset
from modules.quality.quality_inspection import QualityInspection
from modules.website.blog_post import BlogPost

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLAlchemy URL from environment
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()