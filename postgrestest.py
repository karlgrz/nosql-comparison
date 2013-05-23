#!/usr/bin/env python
# encoding: utf=8

import psycopg2 
import logging

class PostgresTest():
	def __init__(self, count):
		self.con = psycopg2.connect("dbname=performancetest user=ubuntu")
		with self.con.cursor() as cur:
		        cur.execute('DELETE FROM items;')
		self.count = count

	def select(self, i):
		with self.con.cursor() as cur:
	                cur.execute("SELECT * FROM items WHERE id = %s", (i,))
	                item = cur.fetchone()
	                self.con.commit()
		
	def insert(self, i):
		with self.con.cursor() as cur:
                	cur.execute("INSERT INTO items (id, value) VALUES(%s, %s)", (i, '{"id": i, "value": {"id": i, "title": "Test Title"}}'))
                	self.con.commit()
