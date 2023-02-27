from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabaseChain, SQLDatabase
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine("duckdb:///:memory:")
# create table
engine.execute("CREATE TABLE src AS SELECT * FROM 'MOCK_DATA.csv';")
db = SQLDatabase(engine=engine)
llm = OpenAI(temperature=0)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
db_chain.run("What's the email address of Guillermo Poxton?")
db_chain.run("How many males are there?")