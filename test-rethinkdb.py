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
if 'items' not in tables:
	logger.debug('starting creating table items')
	r.db('test').table_create('items').run(con)
	logger.debug('finished creating table items')

count = 10000
logger.info('starting performance test #1: insert {0} records'.format(count))
for i in range (1, count):
	r.db('test').table('items').insert({"id": i, "value": {"id": i, "title": "Test Title"}}).run(con, noreply=True)
logger.info('ending performance test #1: insert {0} records'.format(count))
