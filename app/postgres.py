import psycopg2


class PostgresStorage:
    """
    Base class for all classes working with Postgres

    """

    _conn = None
    _cursor = None

    @staticmethod
    def connect(dbname: str, user: str, password: str, host: str, port: int):
        storage = PostgresStorage()
        storage._conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port)
        storage._cursor = storage._conn.cursor()
        return storage

    def get_connection(self):
        return self._conn

    def get_cursor(self):
        return self._cursor


class GroupsStorage(PostgresStorage):

    def __init__(self, storage: PostgresStorage):
        self._conn = storage.get_connection()
        self._cursor = storage.get_cursor()

    def get_groups(self) -> list:
        self._cursor.execute('SELECT * FROM groups')
        groups = self._cursor.fetchall()
        return list(groups)


class PostsStorage(PostgresStorage):

    def __init__(self, storage: PostgresStorage):
        self._conn = storage.get_connection()
        self._cursor = storage.get_cursor()

    def get_posts(self) -> list:
        self._cursor.execute('SELECT * FROM posts')
        posts = self._cursor.fetchall()
        return list(posts)





