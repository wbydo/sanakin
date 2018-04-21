from sqlalchemy import MetaData, Table, Column,\
    Integer, String, Text, ForeignKey, PrimaryKeyConstraint
from migrate import *

meta = MetaData()
file_table = Table(
    'files', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), unique=True),
)

post_table = Table(
    'posts', meta,
    Column('id', Integer),
    Column('contents', Text),
    Column(
        'file_id', Integer,
        ForeignKey('files.id', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    PrimaryKeyConstraint('id', 'file_id')

)

sentence_table = Table(
    'sentences', meta,
    Column('id', Integer, primary_key=True),
    Column('contents', Text),
    Column('post_id', Integer),
    Column('post_file_id', Integer),

    ForeignKeyConstraint(
        ['post_id','post_file_id'],
        ['posts.id', 'posts.file_id']
    )
)

lang_model_file_table = Table(
    'lang_model_files', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), unique=True),
    Column('order', Integer)
)

created_lang_model_table = Table(
    "created_lang_model", meta,
    Column("sentence_id", Integer, ForeignKey("sentences.id", onupdate='CASCADE', ondelete='CASCADE')),
    Column("lang_model_id", Integer, ForeignKey("lang_model_files.id", onupdate='CASCADE', ondelete='CASCADE'))
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    meta.create_all()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    meta.drop_all()
