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

logger.info('starting performance test #1: insert 1000000 records')
for i in range (1, 1000000):
	db.items.save({"id": i, "value": {"id": i, "title": "Test Title"}})
logger.info('ending performance test #1: insert 1000000 records')
