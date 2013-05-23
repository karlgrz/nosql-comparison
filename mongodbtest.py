#!/usr/bin/env python
# encoding: utf=8

import pymongo
import logging

class MongoDBTest():
	def __init__(self, count):
		client = pymongo.MongoClient("localhost", 27017)
		self.db = client.performancetest
		self.count = count
	def select(self, i):
		self.db.items.find_one({"id": i})
	def insert(self, i):
		self.db.items.save({"id": i, "value": {"id": i, "title": "Test Title"}})
