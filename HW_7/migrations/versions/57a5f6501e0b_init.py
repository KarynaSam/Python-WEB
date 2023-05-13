"""'Init'

Revision ID: 57a5f6501e0b
Revises:
Create Date: 2023-05-11 22:25:14.263835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a5f6501e0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('disciplines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('date_of', sa.Date(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('discipline_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['discipline_id'], ['disciplines.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('students')
    op.drop_table('disciplines')
    op.drop_table('teachers')
    op.drop_table('groups')
    # ### end Alembic commands ###