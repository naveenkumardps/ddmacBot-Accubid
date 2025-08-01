"""projects_indlb

Revision ID: c9f551489835
Revises: 28b1335e7a44
Create Date: 2025-08-01 13:41:34.767267

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c9f551489835'
down_revision = '28b1335e7a44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_dirlib')
    op.drop_table('project_inclb')
    op.drop_table('project_lbesc')
    op.create_index(op.f('ix_project_lbfac_id'), 'project_lbfac', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_lbfac_id'), table_name='project_lbfac')
    op.create_table('project_lbesc',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('project_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('escalation_period', mysql.TEXT(), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('percent_of_contract', mysql.TEXT(), nullable=True),
    sa.Column('labor_hours', mysql.TEXT(), nullable=True),
    sa.Column('escalation_percent', mysql.TEXT(), nullable=True),
    sa.Column('escalation_amount', mysql.TEXT(), nullable=True),
    sa.Column('financing_percent', mysql.TEXT(), nullable=True),
    sa.Column('total', mysql.TEXT(), nullable=True),
    sa.Column('code', mysql.TEXT(), nullable=True),
    sa.Column('type', mysql.TEXT(), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name=op.f('project_lbesc_ibfk_1')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('project_lbesc_ibfk_2')),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('project_inclb',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('project_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('hours', mysql.TEXT(), nullable=True),
    sa.Column('rate', mysql.TEXT(), nullable=True),
    sa.Column('sub_total', mysql.TEXT(), nullable=True),
    sa.Column('brdn', mysql.TEXT(), nullable=True),
    sa.Column('frng', mysql.TEXT(), nullable=True),
    sa.Column('brdn_total', mysql.TEXT(), nullable=True),
    sa.Column('frng_total', mysql.TEXT(), nullable=True),
    sa.Column('total', mysql.TEXT(), nullable=True),
    sa.Column('full_rate', mysql.TEXT(), nullable=True),
    sa.Column('code', mysql.TEXT(), nullable=True),
    sa.Column('type', mysql.TEXT(), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name=op.f('project_inclb_ibfk_1')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('project_inclb_ibfk_2')),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('project_dirlib',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('project_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('labour_type', mysql.TEXT(), nullable=False),
    sa.Column('crew', mysql.TEXT(), nullable=True),
    sa.Column('hours', mysql.TEXT(), nullable=True),
    sa.Column('rate', mysql.TEXT(), nullable=True),
    sa.Column('sub_total', mysql.TEXT(), nullable=True),
    sa.Column('brdn', mysql.TEXT(), nullable=True),
    sa.Column('frng', mysql.TEXT(), nullable=True),
    sa.Column('brdn_total', mysql.TEXT(), nullable=True),
    sa.Column('frng_total', mysql.TEXT(), nullable=True),
    sa.Column('total', mysql.TEXT(), nullable=True),
    sa.Column('full_rate', mysql.TEXT(), nullable=True),
    sa.Column('code', mysql.TEXT(), nullable=True),
    sa.Column('type', mysql.TEXT(), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name=op.f('project_dirlib_ibfk_1')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('project_dirlib_ibfk_2')),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ### 