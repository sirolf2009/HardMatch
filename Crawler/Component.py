__author__ = 'gokhankacan'
# Component naar Nodes
from py2neo import neo4j,Node,Relationship,Graph

properties = {}  # Dictionary

def add_property(self, key, property):
    self.properties[key] = property

def print_property(self):
    for key in self.properties:
        print("x: " + key)
        print("p: " + self.properties[key])

def save_component_with_relationships(self):
    component = Node("component")
    for key in self.properties:
        component.properties[key] = self.properties[key]
    store.pull()
    relationship = Relationship(component, 'SOLD_AT', store, price=self.properties['price'])
    neo4j_db.create(component)
    neo4j_db.create(relationship)

neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")
store = Node(type='Store', name='alternate.nl')
neo4j_db.create(store)


"""url = "http://www.alternate.nl"
hardware = get_hardware_page_url(url)
components = get_component_page_url(hardware, url)
links = get_component_links(components, url)
get_component_object(links)"""