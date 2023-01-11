import pandas as pd

data1 = pd.read_csv('data1.csv')
data2 = pd.read_csv('data2.csv')

data = data1.merge(data2, how='left')

data = data.drop(columns=['color', 'language'])

data['director_name'].fillna('N/A', inplace = True)

data['gross'].fillna(0, inplace = True)

data['movie_title'] = data['movie_title'].str.replace('é', 'e')

data['country'] = data['country'].str.upper()
data['country'].replace('UNITED STATES', 'USA', inplace = True)

for i in range(len(data)):
  if data['duration'][i] <= 10 or data['duration'][i] > 300:
    data['duration'][i] = 0

for i in range(len(data)):
  if data['imdb_score'][i] <= 0:
    data['imdb_score'][i] = 0

data[['actors1','actors2','actors3']] = data.actors.str.split(',', expand = True)

data.to_json('1912500913_RezaKurniawan.json')

import pymysql


# Connect to the database
connection = pymysql.connect(host='localhost',
                         user='root',
                         password='12345',
                         db='db_1912500913_RezaKurniawan')


# create cursor
cursor=connection.cursor()

cols = "`,`".join([str(i) for i in data.columns.tolist()])

for i,row in data.iterrows():
    sql = "INSERT INTO `uas_1912500913_RezaKurniawan` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    connection.commit()