package com.hardmatch.checker;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.checker.components.ComponentCPU;
import com.hardmatch.checker.components.ComponentCPUFan;
import com.hardmatch.checker.components.ComponentCase;
import com.hardmatch.checker.components.ComponentGraphicsCard;
import com.hardmatch.checker.components.ComponentMotherboard;
import com.hardmatch.checker.components.ComponentRAM;
import com.hardmatch.checker.components.ComponentStorage;
import com.hardmatch.checker.components.IComponent;
import com.sirolf2009.util.neo4j.rest.RestAPI;

import static com.hardmatch.checker.interfaces.InterfaceStore.*;
import static com.hardmatch.checker.interfaces.InterfaceRelations.*;
import static com.hardmatch.checker.interfaces.InterfaceComponent.*;

public class ComponentChecker {

	private List<IComponent> CPUs;
	private List<IComponent> Graphicscards;
	private List<IComponent> Motherboards;
	private List<IComponent> RAM;
	private List<IComponent> Storage;
	private List<IComponent> CPUFan;
	private List<IComponent> Case;

	public RestAPI restTemp;
	public RestAPI restFinal;

	public static int ThreadCounter = 0;
	public static int ThreadQueue = 0;

	public ComponentChecker(Checker checker) {
		restTemp = checker.restTemp;
		restFinal = checker.restFinal;
		CPUs = new ArrayList<IComponent>();
		Motherboards = new ArrayList<IComponent>();
		Graphicscards = new ArrayList<IComponent>();
		Storage = new ArrayList<IComponent>();
		RAM = new ArrayList<IComponent>();
		CPUFan = new ArrayList<IComponent>();
		Case = new ArrayList<IComponent>();
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
		} else if(component instanceof ComponentCPUFan) {
			CPUFan.add((ComponentCPUFan) component);
		} else if(component instanceof ComponentCase) {
			Case.add((ComponentCase) component);
		}
	}

	public int count() {
		return CPUs.size()+Motherboards.size()+RAM.size()+Graphicscards.size()+Storage.size()+CPUFan.size()+Case.size();
	}

	public void crossCheckAll() {
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking motherboards on CPU");
				crossCheck(Motherboards, CPUs, "Motherboard -> CPU");
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking motherboards on RAM");
				crossCheck(Motherboards, RAM, "Motherboard -> RAM");
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking motherboards on GFX");
				crossCheck(Motherboards, Graphicscards, "Motherboard -> GFX");
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking motherboards on Storage");
				crossCheck(Motherboards, Storage, "Motherboard -> STR");
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking motherboards on CPUFans");
				crossCheck(Motherboards, CPUFan, "Motherboard -> CPF");
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking motherboards on Case");
				crossCheck(Motherboards, Case, "Motherboard -> CAS");
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				Checker.log.info("checking CPUs on CPUFan");
				crossCheck(Motherboards, Case, "CPU -> CPF");
			}
		}).start();
		int lastQueue = 0;
		do {
			try {
				Thread.sleep(10);
				System.out.println(ThreadQueue);
				if(lastQueue == 0) {
					lastQueue = ThreadQueue;
				} else if(lastQueue != ThreadQueue) {
					if(ThreadQueue % 10 == 0) {
						Checker.log.info("Remaining threads: "+ThreadQueue);
					}
					lastQueue = ThreadQueue;
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		} while(ThreadCounter != 0);
		Checker.log.info("done");
	}

	public void crossCheck(List<IComponent> list1, final List<IComponent> list2, String threadName) {
		Checker.log.info(threadName+" checking "+list1.size()+" components on "+list2.size()+" nodes");
		for(int i = 0; i < list1.size(); i++) {
			final IComponent component1 = list1.get(i);
			new Thread(new Runnable() {
				@Override
				public void run() {
					for(final IComponent component2 : list2) {
						ThreadQueue++;
						while(ThreadCounter >= 10) { 
							try {
								Thread.sleep(1000);
							} catch (InterruptedException e) {
								e.printStackTrace();
							} 
						}
						ThreadQueue--;
						ThreadCounter++;
						doCheck(component1, component2);
						ThreadCounter--;
					}
				}
			}).start();
		}
	}

	public void doCheck(IComponent component1, IComponent component2) {
		boolean compatible = component1.isCompatibleWith(component2);
		URI startNodeFinal = restFinal.nodes.fromID(component1.getID());
		URI endNodeFinal = restFinal.nodes.fromID(component2.getID());
		URI relationship = restFinal.relationship.addRelationship(startNodeFinal, endNodeFinal, COMPATABILITY);
		try {
			restFinal.relationship.setRelationshipProperties(relationship, "compatability", compatible);
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
	}

	public URI getOrCreateNode(IComponent component) throws URISyntaxException {
		URI node = null;
		String cypher = "MATCH (n:Component) WHERE n."+MODEL_ID+"=\\\""+component.getModelID()+"\\\" RETURN id(n)";
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

	public void createStoreLinks(JSONArray existingRelationships, URI component) {
		for(Object obj : existingRelationships) {
			try {
				JSONObject existingRelationship = (JSONObject) obj;
				URI endNode = new URI(existingRelationship.get("end").toString());
				String storeName = restTemp.nodes.getProperties(endNode).get(STORE_NAME).toString();
				boolean hasRelation = false;
				for(Object objRelation : restFinal.relationship.getRelationships(component)) {
					JSONObject storeRelationship = (JSONObject) objRelation;
					if(storeRelationship.get("type").toString().equals(SOLD_AT)) {
						URI storeNode = new URI(storeRelationship.get("end").toString());
						if(restFinal.nodes.getProperties(storeNode).get(STORE_NAME).toString().equals(storeName)) {
							hasRelation = true;
							break;
						}
					}
				}
				if(hasRelation) {
					continue;
				}
				JSONObject answer = (JSONObject)restFinal.sendCypher("MATCH (store:Store) WHERE store."+STORE_NAME+"=\\\""+storeName+"\\\" RETURN store, id(store)");
				JSONArray results = (JSONArray) answer.get("results");
				JSONObject firstHit = (JSONObject) results.get(0);
				JSONArray data = (JSONArray) firstHit.get("data");
				URI store = null;
				if(data.size() == 0) {
					store = restFinal.nodes.createNode();
					restFinal.nodes.addLabelToNode(store, LABEL_STORE);
					restFinal.nodes.setNodeProperties(store, restTemp.nodes.getRawProperties(endNode));
				} else {
					JSONObject firstDataHit = (JSONObject) data.get(0);
					JSONArray row = (JSONArray) firstDataHit.get("row");
					long storeID = Long.parseLong(row.get(1).toString());
					store = restFinal.nodes.fromID(storeID);
				}
				URI relationship = restFinal.relationship.addRelationship(component, store, SOLD_AT);
				restFinal.relationship.setRelationshipProperties(relationship, restTemp.relationship.getRelationshipProperties(new URI(existingRelationship.get("self").toString())));
			} catch (URISyntaxException e) {
				e.printStackTrace();
			}
		}
	}

	public void addLabels(URI node, String labels) {
		labels = labels.replace("[", "").replace("]", "").replace("\"", "");
		for(String label : labels.split(",")) {
			restFinal.nodes.addLabelToNode(node, label);
		}
	}

}
