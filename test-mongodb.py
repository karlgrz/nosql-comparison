#!/usr/bin/env python
# encoding: utf=8

import pymongo
import logging

logger = logging.getLogger('mongodb')
file_handler = logging.FileHandler('log/mongodb.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.debug('starting connecting to mongodb')
client = pymongo.MongoClient("localhost", 27017)
logger.debug

db = client.performancetest
logger.debug('db.name={0}'.format(db.name))

count = 10000
logger.info('starting performance test #1: insert {0} records'.format(count))
for i in range (1, count):
	db.items.save({"id": i, "value": {"id": i, "title": "Test Title"}})
logger.info('ending performance test #1: insert {0} records'.format(count))

logger.info('starting performance test #2: reading {0} records'.format(count))
for i in range (1, count):
	item = db.items.find_one({"id": i})
logger.info('ending performance test #2: reading {0} records'.format(count))

heavy_pct_count=9000
logger.info('starting performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))

j = 0
for i in range (count, count*2):
	j+=1
	if j % 9 == 0:
		item = db.items.find_one({"id": i})
		j = 0
	else:
		item = db.items.save({"id": i, "value": {"id": i, "title": "Test Title"}})
logger.info('ending performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, count-heavy_pct_count))

logger.info('starting performance test #4: read heavily ({0} reads, {1} writes)'.format(heavy_pct_count, count-heavy_pct_count))

j = 0
for i in range (count*2, count*3):
	j+=1
	if j % 9 == 0:
		item = db.items.save({"id": i, "value": {"id": i, "title": "Test Title"}})
	else:
		item = db.items.find_one({"id": i})
		j = 0
logger.info('ending performance test #4: read heavily ({0} reads, {1} writes)'.format(heavy_pct_count, count-heavy_pct_count))				
