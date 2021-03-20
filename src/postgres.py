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

    def insert_many(self, insert_query: str, data: List[tuple]):
        cursor = self.conn.cursor()
        try:
            psycopg2.extras.execute_values(
                cursor, insert_query, data)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e


class GroupsStorage(PostgresStorage):

    def get_groups(self) -> List[tuple]:
        query, params = 'SELECT * FROM groups', []
        return list(self.exec_query(query, params))


class PostsStorage(PostgresStorage):

    def get_posts(self) -> List[tuple]:
        query, params = 'SELECT * FROM posts', []
        return list(self.exec_query(query, params))

    def get_unprocessed_posts(self) -> List[tuple]:
        query, params = '''SELECT *
                             FROM posts 
                            WHERE date > (SELECT MAX(date) FROM entities)''', []
        return list(self.exec_query(query, params))


class EntitiesStorage(PostgresStorage):

    def get_entities(self) -> List[tuple]:
        query, params = 'SELECT post_id, type, date, entity FROM entities', []
        return list(self.exec_query(query, params))

    def add_entities(self, entities_list: List[tuple]):
        insert_query = 'INSERT INTO entities(post_id, type, date, entity) VALUES %s'
        self.insert_many(insert_query, entities_list)


class Storage(GroupsStorage, PostsStorage, EntitiesStorage):
    pass
