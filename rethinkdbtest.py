#!/usr/bin/env python
# encoding: utf=8

import rethinkdb as r
import logging

class RethinkDBTest():
	def __init__(self, count):
		self.con = r.connect('localhost', 28015).repl()
		tables = r.db('test').table_list().run(self.con)
		if 'items' in tables:
		        r.db('test').table_drop('items').run(self.con)
		r.db('test').table_create('items').run(self.con)
		self.count = count
	def select(self, i):
		r.db('test').table('items').insert({"id": i, "value": {"id": i, "title": "Test Title"}}).run(self.con, noreply=True)
	def insert(self, i):
		r.db('test').table('items').get(i).run(self.con)	
