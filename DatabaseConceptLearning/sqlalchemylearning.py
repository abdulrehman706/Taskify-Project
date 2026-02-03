import sqlalchemy as sa

engine = sa.create_engine("sqlite:///:memory:")
metadata = sa.MetaData()

user_table = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String)
)
metadata.create_all(engine)