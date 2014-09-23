package com.hardmatch.matcher;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Transaction;

import com.hardmatch.matcher.neo4j.relation.RelationType;

public class Util {

	public static void LinkShopProduct(GraphDatabaseService graph, Node shop, Node product, float price) {
		try (Transaction tx = graph.beginTx()) {            
            shop.createRelationshipTo(product, RelationType.SELLS).setProperty("Price", price+"");
            product.createRelationshipTo(shop, RelationType.SOLD_BY).setProperty("Price", price+"");
            tx.success();
        }
	}
}
