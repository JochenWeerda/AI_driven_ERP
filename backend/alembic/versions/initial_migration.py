"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Benutzer-Tabelle
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('role', sa.Enum('admin', 'manager', 'user', name='userrole'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    
    # Kunden-Tabelle
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('sales_rep_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['sales_rep_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_email'), 'customer', ['email'], unique=True)
    
    # Produkt-Tabelle
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sku', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=True),
        sa.Column('min_stock_level', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_sku'), 'product', ['sku'], unique=True)
    
    # Bestellung-Tabelle
    op.create_table(
        'order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_number', sa.String(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_order_number'), 'order', ['order_number'], unique=True)
    
    # Bestellposition-Tabelle
    op.create_table(
        'orderitem',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Lager-Tabelle
    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('last_restock_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('inventory')
    op.drop_table('orderitem')
    op.drop_index(op.f('ix_order_order_number'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_product_sku'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_customer_email'), table_name='customer')
    op.drop_table('customer')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.execute('DROP TYPE userrole') 