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
r.connect('localhost', 28015).repl()
logger.debug('finished connecting to rethinkdb')

logger.debug('starting creating table items')
r.db('test').table_create('items').run()
logger.debug('finished creating table items')

logger.info('starting performance test #1: insert 1000000 records')
for i in range (1, 1000000):
	r.db('test').table('items').insert({"id": i, "value": {"id": i, "title": "Test Title"}}).run(noreply=True)
logger.info('ending performance test #1: insert 1000000 records')
