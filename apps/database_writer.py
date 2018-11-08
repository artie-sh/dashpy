import sqlite3
import dateparser


class CsvReader:

    db_path = '../prices.sqlite'
    csv_path = '../xrp1.csv'

    def read_file(self, file_name):
        formatted = list()
        csv = open(file_name).read().splitlines()
        for line in csv:
            fline = dict()
            line = line.split(',')
            fline['date'] = dateparser.parse(line[0])
            fline['open'] = line[2]
            fline['high'] = line[3]
            fline['low'] = line[4]
            fline['close'] = line[5]
            formatted.append(fline)
        return formatted

    def connect_db(self, db_path):
        conn = sqlite3.connect(db_path)
        return conn

    def read_db(self, cur, table):
        return list(cur.execute('SELECT * FROM %s ORDER BY date asc' % table))

    def write_line(self, cur, line, table):
        cur.execute('INSERT INTO %s (date, open, high, low, close) VALUES (?, ?, ?, ?, ?)' % table,
                    (line['date'], line['open'], line['high'], line['low'], line['close']))
        print '%s, %s, %s, %s, %s, %s' % (table, line['date'], line['open'], line['high'], line['low'], line['close'])

    def write_csv_to_db(self, csv, db, table):
        conn = self.connect_db(db)
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS %s' % table)
        cur.execute('CREATE TABLE %s (date TEXT, open FLOAT, high FLOAT, low FLOAT, close FLOAT)' % table)
        conn.commit()
        data = self.read_file(csv)
        for line in data[1:]:
            self.write_line(cur, line, table)
        conn.commit()
        conn.close()


#c = CsvReader()
#c.write_csv_to_db(c.csv_path, c.db_path, 'xrp')
# r = c.read_db(c.connect_db(c.db_path))
# for line in r:
#     print line