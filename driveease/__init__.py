import pymysql
pymysql.install_as_MySQLdb()

# Bypass Django 5+ database version check for older MariaDB/MySQL versions
from django.db.backends.base.base import BaseDatabaseWrapper
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# Disable RETURNING syntax for MariaDB versions below 10.5
from django.db.backends.mysql.features import DatabaseFeatures

DatabaseFeatures.can_return_columns_from_insert = property(
    lambda self: self.connection.mysql_is_mariadb and self.connection.mysql_version >= (10, 5, 0)
)
