import psycopg2
import csv
from pathlib import Path


def main():
    host = "postgres"
    database = "postgres"
    user = "postgres"
    pas = "postgres"
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    
    cur = conn.cursor()

    with open("schema.sql", 'r') as f:
        cur.execute(f.read())
        conn.commit()

    with open("data/accounts.csv", 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                insert into accounts values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                int(row['account_id']),
                row[' first_name'],
                row[' last_name'],
                row[' address_1'],
                row[' address_2'],
                row[' city'],
                row[' state'],
                row[' zip_code'],
                row[' join_date']
            ))

    conn.commit()

    with open("data/products.csv", 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
            insert into products values(%s, %s, %s)
        """,
        (
            int(row['product_id']),
            int(row[' product_code']),
            row[' product_description']
        ))
    
    conn.commit()

    with open("data/transactions.csv", 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                insert into transactions values(%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row['transaction_id'],
                row[' transaction_date'],
                int(row[' product_id']),
                int(row[' product_code']),
                row[' product_description'],
                int(row[' quantity']),
                int(row[' account_id'])
            ))

    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
