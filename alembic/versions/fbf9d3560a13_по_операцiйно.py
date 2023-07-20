"""по операцiйно

Revision ID: fbf9d3560a13
Revises: 7694e6259506
Create Date: 2023-07-20 16:25:09.404194

"""
from alembic import op
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Integer, String
from alembic.operations import Operations, MigrateOperation


# revision identifiers, used by Alembic.
revision = 'fbf9d3560a13'
down_revision = '7694e6259506'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("detail_m_k") as batch_op:
        batch_op.add_column(sa.Column('detail_operations_id', sa.Integer(), nullable=True))
        batch_op.create_index(op.f('ix_detail_m_k_id_operations'), ['id'], unique=False)


        batch_op.create_foreign_key('fk_operations_detail', 'detail_operations', ['detail_operations_id'], ['id'])
        batch_op.drop_column('material_id')
        batch_op.drop_column('operation_id')

def downgrade() -> None:
    with op.batch_alter_table("detail_m_k") as batch_op:
        batch_op.add_column(sa.Column('operation_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('material_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint('name_of_your_new_constraint', type_='foreignkey')
        batch_op.create_foreign_key('name_of_your_first_constraint', 'operations', ['operation_id'], ['id'])
        batch_op.create_foreign_key('name_of_your_second_constraint', 'materials', ['material_id'], ['id'])
        batch_op.drop_index(op.f('ix_detail_m_k_id'))
        batch_op.drop_column('detail_operations_id')

