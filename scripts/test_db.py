import psycopg2
import time

# Testing multiple hosts and ports
tests = [
    {"host": "aws-1-eu-west-2.pooler.supabase.com", "port": 5432},
    {"host": "aws-1-eu-west-2.pooler.supabase.com", "port": 6543},
    {"host": "db.owdvtdqsbjxsgmisxhvi.supabase.co", "port": 5432}
]
user = "postgres.owdvtdqsbjxsgmisxhvi"
password = "63KwV-CWGbmZ+Xx"

for test in tests:
    host = test["host"]
    port = test["port"]
    conn_str = f"postgresql://{user}:{password}@{host}:{port}/postgres"
    print(f"Testing connection to {host}:{port}...")
    try:
        start_time = time.time()
        conn = psycopg2.connect(conn_str, connect_timeout=5)
        print(f"Connection to {host}:{port} successful!")
        conn.close()
    except Exception as e:
        print(f"Connection to {host}:{port} failed: {e}")
