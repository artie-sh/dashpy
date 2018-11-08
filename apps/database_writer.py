import sqlite3
import dateparser


class CsvReader:

    db_path = '../prices.sqlite'
    csv_path = 'xrp.csv'

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

    def read_db(self, cur):
        return list(cur.execute('SELECT * FROM xrp ORDER BY date asc'))

    def write_line(self, cur, line):
        cur.execute('INSERT INTO xrp (date, open, high, low, close) VALUES (?, ?, ?, ?, ?)',
                    (line['date'], line['open'], line['high'], line['low'], line['close']))

    def write_csv_to_db(self, csv, db):
        conn = self.connect_db(db)
        cur = conn.cursor()
        data = self.read_file(csv)
        for line in data:
            self.write_line(cur, line)
        conn.commit()
        conn.close()


# c = CsvReader()
# r = c.read_db(c.connect_db(c.db_path))
# for line in r:
#     print line