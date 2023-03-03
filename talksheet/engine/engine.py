from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabaseChain, SQLDatabase
from sqlalchemy import create_engine

load_dotenv()


def read_data_from_csv(question: str, path_to_csv: str):
    engine = create_engine("duckdb:///:memory:")
    # create table
    engine.execute(f"CREATE TABLE src AS SELECT * FROM '{path_to_csv}';")
    db = SQLDatabase(engine=engine)
    llm = OpenAI(temperature=0)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, return_direct=True)
    response = db_chain.run(question)
    return response
