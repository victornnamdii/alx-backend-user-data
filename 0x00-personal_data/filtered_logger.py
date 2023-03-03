#!/usr/bin/env python3
"""A module for filtering logs.
"""

import logging
import os
import re
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    obf_fields = '|'.join(fields)
    find = r'(?P<field>{})=[^{}]*'.format(obf_fields, separator)
    replace = r'\g<field>={}'.format(redaction)
    return re.sub(find, replace, message)


def get_logger() -> logging.Logger:
    """
    get logger
    """
    logger = logging.getLogger('user-data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates connection"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    connector = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_username,
        password=db_password,
        database=db_name
    )
    return connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record"""
        msg = super().format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


def main() -> None:
    """Logs the tables from mysql connection"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)
    data = cursor.fetchall()

    for row in data:
        fields = "name={}; email={}; phone={}; ssn={}; password={}; ip={};\
            last_login={}; user_agent={}".format(row[0], row[1], row[2],
                                                 row[3], row[4], row[5],
                                                 row[6], row[7])
        logger.info(fields)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
