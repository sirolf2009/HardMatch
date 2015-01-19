#!/usr/bin/python
__author__ = 'gokhankacan'
from py2neo import neo4j, Node, Relationship, Graph

db = Graph("http://localhost:7484/db/data/")
db.cypher.execute_one("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r")
print("Temp Database is Cleared")