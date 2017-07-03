import sqlite3
import string

class Repo:
    def __init__(self, dbFile):
        self.__dbFile = dbFile 
        self.__conn = sqlite3.connect(self.__dbFile)
        self.__CreateSchema()

    def __del__(self):
        self.__conn.close()

    def __CreateSchema(self):
        QCREATE = "CREATE TABLE if not exists Log (Id INTEGER PRIMARY KEY ASC, [Date] DATETIME NOT NULL, Temperature FLOAT NOT NULL, Humidity FLOAT NOT NULL)"
        cursor = self.__conn.cursor()
        cursor.execute(QCREATE)
        cursor.close()

    def AddReading(self, temperature, humidity):
        QINSERT = "insert into Log ([Date], Temperature, Humidity) values (datetime(), ?, ?)"
        cursor = self.__conn.cursor()

        reading = (temperature, humidity)
        cursor.execute(QINSERT, reading)
        self.__conn.commit()
        cursor.close()


    @property
    def Readings(self):
        QSELECT = "select Id, [Date], Temperature, Humidity from Log;"
        cursor = self.__conn.cursor()
        readings = []
        for row in cursor.execute(QSELECT):
            readings.append(Reading.FromRow(row))

        cursor.close()
        return readings 


class Reading:
    @staticmethod
    def FromRow(row):
        return Reading(row[0], row[1], row[2], row[3])

    def __init__(self, id, date, temperature, humidity):
        self.Id = id
        self.Date = date
        self.Temperature = temperature
        self.Humidity = humidity
