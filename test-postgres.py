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

with con.cursor() as cur:
	cur.execute('DELETE FROM items;')

count = 10000
logger.info('starting performance test #1: insert {0} records'.format(count))
with con.cursor() as cur:
	for i in range (1, count):
		cur.execute("INSERT INTO items (id, value) VALUES(%s, %s)", (i, '{"id": i, "value": {"id": i, "title": "Test Title"}}'))
		con.commit()
logger.info('ending performance test #1: insert {0} records'.format(count))

logger.info('starting performance test #2: read {0} records'.format(count))
with con.cursor() as cur:
	for i in range (1, count):
		cur.execute("SELECT * FROM items WHERE id = %s", (i,))
		item = cur.fetchone()
		con.commit()
logger.info('ending performance test #2: read {0} records'.format(count))

heavy_pct_count=9000
logger.info('starting performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))
with con.cursor() as cur:
	j = 0 
	for i in range (count, count*2):
		j+=1
               	if j % 9 == 0:
			cur.execute("SELECT * FROM items WHERE id = %s", (i-count,))
	        	item = cur.fetchone()
			con.commit()
			j = 0
                else:
			cur.execute("INSERT INTO items (id, value) VALUES(%s, %s)", (count + i, '{"id": i, "value": {"id": i, "title": "Test Title"}}'))
			con.commit()
logger.info('ending performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))
