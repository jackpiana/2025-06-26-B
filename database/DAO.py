from database.DB_connect import DBConnect
from model.circuito import Circuit
from model.result import Result


class DAO():
    @staticmethod
    def getAllCircuits():
        """
               usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
               return: mappa key= id, value= oggetto
               """
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from circuits c 
                               """
            cursor.execute(query)
            for row in cursor:
                result[row["circuitId"]] = (Circuit(**row))  # **row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result


    @staticmethod
    def getter_anni():
        """
        :return: lista di tuple contenenti gli attributi selezionati dalla query
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select distinct year
                        from seasons s 
                        order by year desc
        """
            cursor.execute(query)
            for row in cursor:
                result.append(row[0])  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_resCirYear(year, circuitId):
        """
        return tutti i risultati di un anno su un circuito
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select re.*
                        from results re, races ra, circuits c 
                        where re.raceId = ra.raceId 
                        and ra.circuitId = c.circuitId 
                        and ra.`year`  = %s
                        and ra.circuitId = %s
                            """
            cursor.execute(query, (year, circuitId))
            for row in cursor:
                result.append(Result(**row))  # **row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_edges(year1, year2):
        """
        :return: lista di tuple contenenti n1, n2 nodi che compongono la edge
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select *
                        from (select circuitId as cid1
                        from races ra
                        where year > %s 
                        and year < %s ) t1,
                        (select circuitId as cid2
                        from races ra
                        where year > %s  
                        and year < %s ) t2
                        where t1.cid1>t2.cid2
                        group by t1.cid1, t2.cid2
           """
            cursor.execute(query, (year1, year2, year1, year2))
            for row in cursor:
                result.append(row)  # row è una tupla contenente n1, n2
            cursor.close()
            conn.close()
        return result


    @staticmethod
    def getter_numeroGare_inRange(circuitId, yearInf, yearSup):
        """
        :return: lista di tuple contenenti gli attributi selezionati dalla query
        """
        conn = DBConnect.get_connection()
        result = 0
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """
            select count(distinct raceId)
            from races r 
            where circuitId = %s
            and year > %s
            and year < %s
            """
            cursor.execute(query, (circuitId, yearInf, yearSup))
            for row in cursor:
                result += row[0] #row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result
