"""reminders repeat

Revision ID: 5606614f409d
Revises: 9638fcf55593
Create Date: 2022-04-11 15:25:26.679061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5606614f409d'
down_revision = '9638fcf55593'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminders', sa.Column('is_repeat', sa.Boolean(), nullable=True))
    op.add_column('reminders', sa.Column('repeat_count', sa.Integer(), nullable=True))
    op.add_column('reminders', sa.Column('curr_repeat', sa.Integer(), nullable=True))
    op.add_column('reminders', sa.Column('repeat_until', sa.DateTime(), nullable=True))
    op.add_column('reminders', sa.Column('repeat_range', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reminders', 'repeat_range')
    op.drop_column('reminders', 'repeat_until')
    op.drop_column('reminders', 'curr_repeat')
    op.drop_column('reminders', 'repeat_count')
    op.drop_column('reminders', 'is_repeat')
    # ### end Alembic commands ###
