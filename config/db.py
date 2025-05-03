from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:miximala@192.168.123.52:3306/testdb", echo = True)

meta = MetaData()

conn = engine.connect()
conn.execution_options()

