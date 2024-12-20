"""Add code to Build model

Revision ID: 552afc0d3b8d
Revises: a4b988485165
Create Date: 2024-12-04 21:32:58.737635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '552afc0d3b8d'
down_revision = 'a4b988485165'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    op.drop_table('build')
    op.drop_table('build_perk')
    op.drop_table('user')
    op.drop_table('perk')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('perk',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), nullable=False),
    sa.Column('image', sa.VARCHAR(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('build_perk',
    sa.Column('build_id', sa.INTEGER(), nullable=False),
    sa.Column('perk_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['build_id'], ['build.id'], name='fk_build_perk_build_id_build'),
    sa.ForeignKeyConstraint(['perk_id'], ['perk.id'], name='fk_build_perk_perk_id_perk'),
    sa.PrimaryKeyConstraint('build_id', 'perk_id')
    )
    op.create_table('build',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('priority', sa.INTEGER(), nullable=True),
    sa.Column('folder_path', sa.VARCHAR(length=200), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_build_user_id_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('build_id', sa.INTEGER(), nullable=False),
    sa.Column('vote_type', sa.VARCHAR(length=10), nullable=False),
    sa.ForeignKeyConstraint(['build_id'], ['build.id'], name='fk_vote_build_id_build'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_vote_user_id_user'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
