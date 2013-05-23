#!/usr/bin/env python
# encoding: utf=8

import logging, datetime
from mongodbtest import *
from rethinkdbtest import *
from postgrestest import *

logger = logging.getLogger('tests')
file_handler = logging.FileHandler('log/tests.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

count = 10000
tests = [MongoDBTest(count), RethinkDBTest(count), PostgresTest(count)]

for test in tests:
	classname = test.__class__.__name__
	logger.info('Starting {0} tests...'.format(classname))
	suitestart = datetime.datetime.now()
	test1start = datetime.datetime.now()
	logger.info('starting performance test #1: insert {0} records'.format(test.count))
	for i in range (1, test.count):
		test.insert(i)
	test1duration = datetime.datetime.now() - test1start
	logger.info('ending performance test #1: insert {0} records, Duration: {1} seconds'.format(test.count, test1duration.total_seconds()))

	test2start = datetime.datetime.now()
	logger.info('starting performance test #2: reading {0} records'.format(test.count))
	for i in range (1, test.count):
		item = test.select(i)
	test2duration = datetime.datetime.now() - test2start
	logger.info('ending performance test #2: reading {0} records, Duration: {1} seconds'.format(test.count, test2duration.total_seconds()))
	
	heavy_pct_count=9000
	test3start = datetime.datetime.now()
	logger.info('starting performance test #3: write heavily ({0} writes, {1} reads)'.format(heavy_pct_count, test.count-heavy_pct_count))
	
	j = 0
	for i in range (test.count, test.count*2):
		j+=1
		if j % 9 == 0:
			item = test.select(i)
			j = 0
		else:
			item = test.insert(i)
	test3duration = datetime.datetime.now() - test3start
	logger.info('ending performance test #3: write heavily ({0} writes, {1} reads), Duration: {2} seconds'.format(heavy_pct_count, test.count-heavy_pct_count, test3duration.total_seconds()))
	
	test4start = datetime.datetime.now()
	logger.info('starting performance test #4: read heavily ({0} reads, {1} writes)'.format(heavy_pct_count, test.count-heavy_pct_count))
	
	j = 0
	for i in range (test.count*2, test.count*3):
		j+=1
		if j % 9 == 0:
			item = test.insert(i)
		else:
			item = test.select(i)
			j = 0
	test4duration = datetime.datetime.now() - test4start
	logger.info('ending performance test #4: read heavily ({0} reads, {1} writes), Duration: {2} seconds'.format(heavy_pct_count, test.count-heavy_pct_count, test4duration.total_seconds() ))

	totalduration = datetime.datetime.now() - suitestart
	logger.info('Ending {0} tests, Total Duration: {1} seconds'.format(classname, totalduration.total_seconds()))
