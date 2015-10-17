import re
import sqlite3 as sql
connection = sql.connect('wiki.db')
cursor = connection.cursor()


def articles_description():
    cursor.execute('''
    CREATE TABLE Wiki(
    Word TEXT,
    Number INTEGER
    );
    ''')
    with open('udmwiki-20150901-pages-articles-multistream.xml', 'r', encoding='utf-8') as f:
        for line in f:
            if "'''" in line[0:4]:
                while '</text>' not in line:
                    r = re.findall('[а-яӝӟӥӧӵёa-z]+[\-]*?[а-яӝӟӥӧӵёa-z]*', line.lower())
                    for word in r:
                        cursor.execute("SELECT count(*) FROM Wiki WHERE Word = ?", (word,))
                        data = cursor.fetchone()[0]
                        if data == 0:
                            cursor.execute('INSERT INTO Wiki VALUES(?,?)', (word,1))
                            connection.commit()
                        else:
                            cursor.execute('UPDATE Wiki SET Number = Number + 1 WHERE Word = ?', (word,))
                            connection.commit()
                    line = next(f)
    connection.commit()


articles_description()