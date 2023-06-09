"""empty message

Revision ID: 662fc3395459
Revises: b08322495ba4
Create Date: 2023-04-25 12:30:36.176344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662fc3395459'
down_revision = 'b08322495ba4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo_posts', sa.Column('creator_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'photo_posts', 'users', ['creator_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photo_posts', type_='foreignkey')
    op.drop_column('photo_posts', 'creator_id')
    # ### end Alembic commands ###
