"""Initial

Revision ID: c92501b80749
Revises:
Create Date: 2022-11-07 21:50:10.309910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c92501b80749'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'chats',
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column('chatname', sa.VARCHAR(length=32), nullable=True),
        sa.Column('reg_date', sa.DATE(), nullable=True),
        sa.Column('upd_date', sa.DATE(), nullable=True),
        sa.PrimaryKeyConstraint('chat_id'),
        sa.UniqueConstraint('chat_id')
    )
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('username', sa.VARCHAR(length=32), nullable=True),
        sa.Column('reg_date', sa.DATE(), nullable=True),
        sa.Column('upd_date', sa.DATE(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('chats')
    # ### end Alembic commands ###