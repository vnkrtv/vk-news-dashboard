from typing import List, Generator

import psycopg2


class PostgresStorage:
    """
    Base class for all classes working with Postgres

    """

    conn: psycopg2.extensions.connection

    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    @classmethod
    def connect(cls, dbname: str, user: str, password: str, host: str, port: int):
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port)
        return cls(conn=conn)

    def exec_query(self, query: str, params: list) -> Generator:
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e
        return cursor.fetchall()


class GroupsStorage(PostgresStorage):

    def get_groups(self) -> List[tuple]:
        query, params = 'SELECT * FROM groups', []
        return list(self.exec_query(query, params))


class PostsStorage(PostgresStorage):

    def get_posts(self) -> List[tuple]:
        query, params = 'SELECT * FROM posts', []
        return list(self.exec_query(query, params))
