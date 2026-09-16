"""initial schema

Revision ID: 1317c64123b7
Revises: 
Create Date: 2026-09-16 16:34:04.809004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1317c64123b7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('date', sa.String(length=100), nullable=False),
        sa.Column('read_time', sa.String(length=50), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('image', sa.Text(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_blogs_slug', 'blogs', ['slug'], unique=True)
    op.create_index('ix_blogs_category', 'blogs', ['category'])

    op.create_table(
        'services',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('subtitle', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon', sa.String(length=100), nullable=False),
        sa.Column('video_url', sa.Text(), nullable=False),
        sa.Column('full_description', sa.Text(), nullable=False),
    )

    op.create_table(
        'packages',
        sa.Column('id', sa.String(length=50), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=False),
        sa.Column('sessions', sa.Integer(), nullable=False),
        sa.Column('price', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('ideal', sa.Text(), nullable=False),
        sa.Column('features', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('popular', sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        'testimonials',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('image', sa.Text(), nullable=False),
    )

    op.create_table(
        'team_members',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('image', sa.Text(), nullable=False),
    )

    op.create_table(
        'faqs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
    )

    op.create_table(
        'contacts',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='new'),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'status_checks',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('client_name', sa.String(length=255), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('status_checks')
    op.drop_table('contacts')
    op.drop_table('faqs')
    op.drop_table('team_members')
    op.drop_table('testimonials')
    op.drop_table('packages')
    op.drop_table('services')
    op.drop_index('ix_blogs_category', table_name='blogs')
    op.drop_index('ix_blogs_slug', table_name='blogs')
    op.drop_table('blogs')
