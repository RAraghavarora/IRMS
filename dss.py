import MySQLdb

def execute_query(sql_query):
    '''
    Helper Function that takes a SQL query and returns the executed output
    '''
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="igcarlibrary",
        db="library"
    )
    cur = db.cursor()

    try:
        cur.execute(sql_query)
        return cur.fetchall()
    except MySQLdb.Error as e:
        print(e)
        return 'Error'


biblio_list = Biblio.objects.all()

total_books=[0]
no_of_copies = []
for biblio in biblio_list:
    try:
        items = biblio.items_set.all()
        circulation_book = False

        for item in items:
            if not circulation_book and item.itype in ('R', 'SPR', 'STB', 'DIVB', 'C'):
                circulation_book = True

        if any(item.itype in ('R', 'SPR', 'STB', 'DIVB', 'C') for item in items):
            total_books[0]+=1


        else:
            continue
    except Exception as e:
        print(e)
        continue
