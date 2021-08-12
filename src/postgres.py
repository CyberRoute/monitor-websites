import psycopg2


class Postgres:
    """Postgres object"""
    def __init__(self, host, db, user, password, table):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.table = table

    def cursor(self):
        """Open cursor"""
        uri = f'postgres://{self.user}:' \
              f'{self.password}@{self.host}:18156/{self.db}?sslmode=require'
        conn = psycopg2.connect(uri)
        conn.autocommit = True
        return conn.cursor()

    def db_insert(self, url, status, resp, time):
        """DB insert"""
        self.cursor().execute(f'INSERT INTO {self.table} '
                              '(site_url, http_status, response_time_ms, time) '
                              'VALUES (%s, %s, %s, %s)', (url, status, resp, time,))
