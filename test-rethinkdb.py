#!/usr/bin/env python
# encoding: utf=8

import rethinkdb as r
import logging

logger = logging.getLogger('rethinkdb')
file_handler = logging.FileHandler('log/rethinkdb.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.debug('starting connecting to rethinkdb')
con = r.connect('localhost', 28015).repl()
logger.debug('finished connecting to rethinkdb')

tables = r.db('test').table_list().run(con)
print tables
if 'items' in tables:
	r.db('test').table_drop('items').run(con)

logger.debug('starting creating table items')
r.db('test').table_create('items').run(con)
logger.debug('finished creating table items')

count = 10000
logger.info('starting performance test #1: insert {0} records'.format(count))
for i in range (1, count):
	r.db('test').table('items').insert({"id": i, "value": {"id": i, "title": "Test Title"}}).run(con, noreply=True)
logger.info('ending performance test #1: insert {0} records'.format(count))

logger.info('starting performance test #2: read {0} records'.format(count))
for i in range (1, count):
	item = r.db('test').table('items').get(i).run(con)
logger.info('ending performance test #2: read {0} records'.format(count))

heavy_pct_count=9000
logger.info('starting performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))
j=0
for i in range (count, count*2):
	j+=1
	if j % 9 == 0:
		item = r.db('test').table('items').get(i).run(con)
		j=0
        else:
		r.db('test').table('items').insert({"id": i, "value": {"id": i, "title": "Test Title"}}).run(con, noreply=True)
logger.info('ending performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))

logger.info('starting performance test #4: read heavily ({0} reads, {1} writes)'.format(heavy_pct_count, count-heavy_pct_count))
j=0
for i in range (count*2, count*3):
	j+=1
	if j % 9 == 0:
		r.db('test').table('items').insert({"id": i, "value": {"id": i, "title": "Test Title"}}).run(con, noreply=True)
		j=0
        else:
		item = r.db('test').table('items').get(i).run(con)
logger.info('ending performance test #4: read heavily ({0} reads, {1} writes)'.format(heavy_pct_count, count-heavy_pct_count))

