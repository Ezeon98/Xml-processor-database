#!/usr/bin/env python3
# pylint: disable=invalid-name,missing-function-docstring,broad-except,missing-module-docstring
import logging
import sys
import os
import time

import debugpy
import psycopg2

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_logger = logging.getLogger(__name__)

POSTGRES = "postgres"


class Database:
    """Database"""

    connection = False
    engine = False
    session = False
    base = False
    pg_host = "db"
    pg_port = 5432
    pg_db = ""
    pg_user = ""
    pg_password = ""

    def __init__(self):
        self.pg_host = os.getenv("PG_HOST")
        self.pg_port = os.getenv("PG_PORT")
        self.pg_db = os.getenv("PG_DB")
        self.pg_user = os.getenv("PG_USER")
        self.pg_password = os.getenv("PG_PASSWORD")

        try:
            _logger.info(f"Connect to DB {self.pg_host}")
            self.connection = psycopg2.connect(
                database=POSTGRES,
                user=self.pg_user,
                password=self.pg_password,
                host=self.pg_host,
                port=self.pg_port,
            )
            self.connection.autocommit = True
        except Exception as error:
            _logger.error(f"Database connection error: {error}")
            raise error

    def check_db(self):
        """Check DB"""
        connection = False
        try:
            _logger.info(f"Connect to DB {self.pg_host}")
            connection = psycopg2.connect(
                database=self.pg_db,
                user=self.pg_user,
                password=self.pg_password,
                host=self.pg_host,
                port=self.pg_port,
            )
        except Exception as e:
            _logger.error(f"Database connection error: {e}")
        return connection

    def create_db(self):
        with self.connection.cursor() as cursor:
            _logger.debug(f"Creating Database: {self.pg_db}")
            cursor.execute(f"CREATE DATABASE {self.pg_db};")


if __name__ == "__main__":
    debug = os.getenv("DEBUG", "false")
    debug_port = os.getenv("DEBUG_PORT", "3002")

    if debug == "true":
        _logger.info(f"====Starting Debugpy at {debug_port}===")
        debugpy.listen(("0.0.0.0", int(debug_port)))
        _logger.info("Wait for client....")
        debugpy.wait_for_client()
        debugpy.breakpoint()
        _logger.info("Debugging....")

    start_time = time.time()
    database = False

    while (time.time() - start_time) < 30:
        try:
            database = Database()
            if not database.check_db():
                database.create_db()
            database.connection.close()
            break
        except psycopg2.OperationalError:
            pass
        time.sleep(1)
