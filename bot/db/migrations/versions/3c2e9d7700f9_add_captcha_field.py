"""add captcha field

Revision ID: 3c2e9d7700f9
Revises: 5e71a6dd6ffb
Create Date: 2022-11-15 13:20:28.546971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c2e9d7700f9'
down_revision = '5e71a6dd6ffb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'chats', ['chat_id'])
    op.add_column('users', sa.Column('captcha', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'captcha')
    op.drop_constraint(None, 'chats', type_='unique')
    # ### end Alembic commands ###
