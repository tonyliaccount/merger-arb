def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def last_date(conn, )

def list_to_db(db, articles: list):
    # Process the list using Spacy
    deals = spacy_nlp.name_and_amount(articles)
    # Add missing deals into the database
    for d in deals:
        data_tuple = (d[0], d[1], d[2], d[3])
        db.execute("INSERT INTO financings(Datetime, Title, Borrower,"
                   + "Amount) VALUES(?,?,?,?);", data_tuple)

conn = create_connection('deals.db')
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS financings(
                                    id integer PRIMARY KEY,
                                    DateTime text NOT NULL,
                                    Title text NOT NULL,
                                    Borrower text NOT NULL,
                                    Amount float
                                ); """
if conn is not None:
    create_table(conn, sql_create_projects_table)
fp = r'C:\Users\Adam\OneDrive\HSA\Resources\JuniorMiningNetwork\Financing'
j_list = json_to_list(fp)
cur = conn.cursor()
list_to_db(cur, j_list)
conn.commit()
conn.close()