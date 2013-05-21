#!/usr/bin/env python
# encoding: utf=8

import psycopg2 
import logging

logger = logging.getLogger('postgres')
file_handler = logging.FileHandler('log/postgres.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.debug('starting connecting to postgres')
con = psycopg2.connect("dbname=performancetest user=ubuntu")
logger.debug('finished connecting to postgres')

cur = con.cursor()

cur.execute('DELETE FROM items;')
con.commit()

count = 10000
logger.info('starting performance test #1: insert {0} records'.format(count))
for i in range (1, count):
	cur.execute("INSERT INTO items (id, value) VALUES(%i, %s)", i, '{"id": i, "value": {"id": i, "title": "Test Title"}}')
con.commit()
logger.info('ending performance test #1: insert {0} records'.format(count))

logger.info('starting performance test #2: read {0} records'.format(count))
for i in range (1, count):
	cur.execute('SELECT * FROM items WHERE id = %i', i)
	item = cur.fetchone() 
logger.info('ending performance test #2: read {0} records'.format(count))

heavy_pct_count=9000
logger.info('starting performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))
for i in range (1, count):
        for j in range (1, 9):
                if j % 9 == 0:
			cur.execute('SELECT * FROM items WHERE id = %i', i)
	        	item = cur.fetchone()	
                else:
			cur.execute("INSERT INTO items (id, value) VALUES(%i, %s)", i, '{"id": i, "value": {"id": i, "title": "Test Title"}}')
logger.info('ending performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))

