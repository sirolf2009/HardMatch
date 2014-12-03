package com.hardmatch.checker;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.checker.components.ComponentCPU;
import com.hardmatch.checker.components.ComponentGraphicsCard;
import com.hardmatch.checker.components.ComponentMotherboard;
import com.hardmatch.checker.components.ComponentRAM;
import com.hardmatch.checker.components.ComponentStorage;
import com.hardmatch.checker.components.IComponent;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class ComponentChecker {

	private List<IComponent> CPUs;
	private List<IComponent> Graphicscards;
	private List<IComponent> Motherboards;
	private List<IComponent> RAM;
	private List<IComponent> Storage;

	public RestAPI restTemp;
	public RestAPI restFinal;

	public ComponentChecker(Checker checker) {
		restTemp = checker.restTemp;
		restFinal = checker.restFinal;
		CPUs = new ArrayList<IComponent>();
		Motherboards = new ArrayList<IComponent>();
		Graphicscards = new ArrayList<IComponent>();
		Storage = new ArrayList<IComponent>();
		RAM = new ArrayList<IComponent>();
	}

	public void addComponentToSetup(IComponent component) {
		if(component instanceof ComponentCPU) {
			CPUs.add((ComponentCPU) component);
		} else if(component instanceof ComponentMotherboard) {
			Motherboards.add((ComponentMotherboard) component);
		} else if(component instanceof ComponentRAM) {
			RAM.add((ComponentRAM) component);
		} else if(component instanceof ComponentGraphicsCard) {
			Graphicscards.add((ComponentGraphicsCard) component);
		} else if(component instanceof ComponentStorage) {
			Storage.add((ComponentStorage) component);
		}
	}

	public void crossCheckAll() {
		System.out.println("checking motherboards on CPU");
		crossCheck(Motherboards, CPUs);
		System.out.println("checking motherboards on RAM");
		crossCheck(Motherboards, RAM);
		System.out.println("checking motherboards on Graphics Cards");
		crossCheck(Motherboards, Graphicscards);
		System.out.println("checking motherboards on Storages");
		crossCheck(Motherboards, Storage);
	}

	public void crossCheck(List<IComponent> list1, List<IComponent> list2) {
		for(IComponent component1 : list1) {
			for(IComponent component2 : list2) {
				try {
					boolean compatible = component1.isCompatibleWith(component2);
					System.out.println(compatible);
					URI startNodeFinal = getOrCreateNode(component1);
					URI endNodeFinal = getOrCreateNode(component2);
					createStoreLinks(restTemp.relationship.getRelationships(restTemp.nodes.fromID(component1.getID())), startNodeFinal);
					createStoreLinks(restTemp.relationship.getRelationships(restTemp.nodes.fromID(component2.getID())), endNodeFinal);
					if(compatible) {
						restFinal.relationship.addRelationship(startNodeFinal, endNodeFinal, "COMPATIBLE");
					} else {
						System.out.println("Creating a not compatible relationship");
						restFinal.relationship.addRelationship(startNodeFinal, endNodeFinal, "NOT_COMPATIBLE");
					}
				} catch(URISyntaxException e) {
					e.printStackTrace();
				}
			}
		}
	}

	public URI getOrCreateNode(IComponent component) throws URISyntaxException {
		URI node = null;
		String cypher = "MATCH (n:Component) WHERE n.modelID=\\\""+component.getModelID()+"\\\" RETURN id(n)";
		JSONObject answer = restFinal.sendCypher(cypher);
		JSONArray result = (JSONArray) answer.get("results");
		if(result.size() == 0 || ((JSONArray) ((JSONObject) result.get(0)).get("data")).size() == 0) {
			node = restFinal.nodes.createNode();
			addLabels(node, component.getLabels());
			restFinal.nodes.setNodeProperties(node, restTemp.nodes.getRawProperties(restTemp.nodes.fromID(component.getID())));
		} else {
			JSONArray data = (JSONArray) ((JSONObject) result.get(0)).get("data");
			JSONArray row = (JSONArray) ((JSONObject) data.get(0)).get("row");
			String ID = row.get(0).toString();
			node = restFinal.nodes.fromID(Long.parseLong(ID));
		}
		return node;
	}

	public List<URI> createStoreLinks(JSONArray jsonResult, URI component) {
		for(Object obj : jsonResult) {
			try {
				JSONObject object = (JSONObject) obj;
				URI endNode = new URI(object.get("end").toString());
				String storeName = restTemp.nodes.getProperties(endNode).get("name").toString();
				JSONObject answer = (JSONObject)restFinal.sendCypher("MATCH (store:Store) WHERE store.name=\\\""+storeName+"\\\" RETURN store, id(store)");
				JSONArray results = (JSONArray) answer.get("results");
				JSONObject firstHit = (JSONObject) results.get(0);
				JSONArray data = (JSONArray) firstHit.get("data");
				URI store = null;
				if(data.size() == 0) {
					store = restFinal.nodes.createNode();
					restFinal.nodes.addLabelToNode(store, "Store");
					restFinal.nodes.setNodeProperties(store, restTemp.nodes.getRawProperties(endNode));
				} else {
					JSONObject firstDataHit = (JSONObject) data.get(0);
					JSONArray row = (JSONArray) firstDataHit.get("row");
					long storeID = Long.parseLong(row.get(1).toString());
					store = restFinal.nodes.fromID(storeID);
				}
				URI relationship = restFinal.relationship.addRelationship(component, store, "SOLD_AT");
				restFinal.relationship.setRelationshipProperties(relationship, restTemp.relationship.getRelationshipProperties(new URI(object.get("self").toString())));
			} catch (URISyntaxException e) {
				e.printStackTrace();
			}
		}
		return null;
	}

	public void addLabels(URI node, String labels) {
		labels = labels.replace("[", "").replace("]", "").replace("\"", "");
		for(String label : labels.split(",")) {
			restFinal.nodes.addLabelToNode(node, label);
		}
	}

}