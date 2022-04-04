"""table name change

Revision ID: 77d37d17e066
Revises: d60a09f50f22
Create Date: 2022-04-01 15:42:17.286696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77d37d17e066'
down_revision = 'd60a09f50f22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reminders',
    sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('is_reminded', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('reminder')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reminder',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('text', sa.VARCHAR(), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.Column('is_reminded', sa.BOOLEAN(), nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('reminders')
    # ### end Alembic commands ###