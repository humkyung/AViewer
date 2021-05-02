# coding: utf-8
""" This is document data(SDI) class """

import sys
import os
import sqlite3
from enum import Enum

from qt import *
import networkx as nx

from SingletonInstance import SingletonInstane


class Config:
    def __init__(self, section, key, value):
        self.section = section
        self.key = key
        self.value = value

    '''
        @brief  return size value string
        @author humkyung
        @date   2018.04.24
    '''

    def sizeValue(self):
        return self.inchStr if 'Inch' == self.sizeUnit else self.metricStr


'''
    @brief  Pipe color class
'''


class Color:
    def __init__(self, index, red, green, blue):
        self.index = index
        self.red = red
        self.green = green
        self.blue = blue


'''
    @brief      MessageType
    @author     humkyung 
    @date       2018.07.31
'''


class MessageType(Enum):
    Normal = 1
    Error = 2


class AppDocData(SingletonInstane):

    def __init__(self):

        self.normals = {}
        self.tangents = {}

        self.nodes_data = None
        self.elements_data = None

        self.__g = nx.Graph()

    @property
    def g(self):
        """
        return graph
        """

        return self.__g

    def get_app_db_path(self):
        """Get application DB file path in ProgramData"""
        from App import App

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        app_database = os.path.join(path, 'App.db')
        return app_database

    def buildAppDatabase(self):
        """build application database"""
        from App import App

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        appDatabaseFilePath = os.path.join(path, 'App.db')

        # Creates or opens a file called mydb with a SQLite3 DB
        conn = sqlite3.connect(appDatabaseFilePath)
        with conn:
            try:
                # Get a cursor object
                cursor = conn.cursor()

                sqlFiles = ['App.Configuration.sql', 'App.Styles.sql']
                for sqlFile in sqlFiles:
                    filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Scripts', sqlFile)
                    try:
                        file = QFile(filePath)
                        file.open(QFile.ReadOnly)
                        sql = file.readAll()
                        sql = str(sql, encoding='utf8')
                        cursor.executescript(sql)
                    finally:
                        file.close()
                conn.commit()
            # Catch the exception
            except Exception as ex:
                # Roll back any change if something goes wrong
                conn.rollback()
                print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                          sys.exc_info()[-1].tb_lineno))
        configs = [Config('app', 'mode', 'advanced'), Config('app', 'error origin point', '51,72')]
        self.save_app_configs(configs)

    def loadAppStyle(self):
        """load app style"""
        style = 'Fusion'
        from App import App

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        if not os.path.exists(path):
            os.makedirs(path)

        self.buildAppDatabase()
        try:
            appDatabaseFilePath = os.path.join(path, 'App.db')
            # Creates or opens a file called mydb with a SQLite3 DB
            conn = sqlite3.connect(appDatabaseFilePath)
            # Get a cursor object
            cursor = conn.cursor()

            sql = "select Value from Configuration where Section='App' and Key='Style'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            style = rows[0][0] if 1 == len(rows) else 'Fusion'
        # Catch the exception
        except Exception as ex:
            # Roll back any change if something goes wrong
            conn.rollback()
            print('error occured({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                      sys.exc_info()[-1].tb_lineno))
        finally:
            # Close the db connection
            conn.close()

        return style

    def loadAppStyles(self):
        """load app styles and then return a list"""
        styles = []

        try:
            self.buildAppDatabase()

            path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
            appDatabaseFilePath = os.path.join(path, 'App.db')

            # Creates or opens a file called mydb with a SQLite3 DB
            conn = sqlite3.connect(appDatabaseFilePath)
            # Get a cursor object
            cursor = conn.cursor()

            sql = 'select UID,Value from Styles'
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows: styles.append(row[1])
            if 0 == len(rows): rows.append('fusion')
        # Catch the exception
        except Exception as ex:
            # Roll back any change if something goes wrong
            conn.rollback()
            print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                      sys.exc_info()[-1].tb_lineno))
        finally:
            # Close the db connection
            conn.close()

        return styles

    def getAppConfigs(self, section, key=None):
        """get application configurations"""

        res = []

        # Creates or opens a file called mydb with a SQLite3 DB
        dbPath = self.get_app_db_path()
        conn = sqlite3.connect(dbPath)
        with conn:
            try:
                # Get a cursor object
                cursor = conn.cursor()

                if key is not None:
                    sql = "select * from configuration where section=? and key=?"
                    param = (section, key)
                else:
                    sql = "select * from configuration where section=?"
                    param = (section,)

                cursor.execute(sql, param)
                rows = cursor.fetchall()
                for row in rows:
                    res.append(Config(row[0], row[1], row[2]))
            # Catch the exception
            except Exception as ex:
                print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                          sys.exc_info()[-1].tb_lineno))

        return res

    def save_app_configs(self, configs):
        """save application configurations"""

        # Creates or opens a file called mydb with a SQLite3 DB
        dbPath = self.get_app_db_path()
        conn = sqlite3.connect(dbPath)
        with conn:
            try:
                # Get a cursor object
                cursor = conn.cursor()

                for config in configs:
                    value = config.value
                    if type(value) is str and "'" in value:
                        value = value.replace("'", "''")

                    sql = "insert or replace into configuration values(?,?,?)"
                    param = (config.section, config.key, value)

                    cursor.execute(sql, param)
                conn.commit()
            # Catch the exception
            except Exception as ex:
                # Roll back any change if something goes wrong
                conn.rollback()
                print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                          sys.exc_info()[-1].tb_lineno))

    def deleteAppConfigs(self, section, key=None):
        """delete application configurations"""

        # Creates or opens a file called mydb with a SQLite3 DB
        dbPath = self.get_app_db_path()
        conn = sqlite3.connect(dbPath)
        with conn:
            try:
                # Get a cursor object
                cursor = conn.cursor()

                if key is not None:
                    sql = "delete from configuration where section='{}' and key='{}'".format(section, key)
                else:
                    sql = "delete from configuration where section='{}'".format(section)
                cursor.execute(sql)

                conn.commit()
            # Catch the exception
            except Exception as ex:
                # Roll back any change if something goes wrong
                conn.rollback()
                print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                          sys.exc_info()[-1].tb_lineno))

if __name__ == '__main__':
    from AppDocData import AppDocData

    instance = AppDocData.instance()
