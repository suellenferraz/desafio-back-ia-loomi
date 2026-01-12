"""Add pgvector extension and embedding column

Revision ID: a1b2c3d4e5f6
Revises: 36646653677f
Create Date: 2026-01-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '36646653677f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Criar extensão pgvector
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Adicionar coluna embedding na tabela paints (tipo vector do pgvector)
    # Dimensão 1536 para text-embedding-3-small da OpenAI
    op.execute("""
        ALTER TABLE paints 
        ADD COLUMN IF NOT EXISTS embedding vector(1536)
    """)
    
    # Criar índice para busca semântica
    # Nota: ivfflat requer dados na tabela, então criamos um índice simples primeiro
    # O índice ivfflat pode ser criado depois quando houver dados suficientes
    op.execute("""
        CREATE INDEX IF NOT EXISTS paints_embedding_idx 
        ON paints 
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Remover índice
    op.execute('DROP INDEX IF EXISTS paints_embedding_idx')
    
    # Remover coluna embedding
    op.drop_column('paints', 'embedding')
    
    # Não removemos a extensão pgvector pois pode ser usada por outras tabelas
