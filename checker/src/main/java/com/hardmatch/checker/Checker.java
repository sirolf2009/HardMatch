package com.hardmatch.checker;

import static com.hardmatch.checker.interfaces.InterfaceComponent.MODEL_ID;
import static com.hardmatch.checker.interfaces.InterfaceRelations.SOLD_AT;
import static com.hardmatch.checker.interfaces.InterfaceStore.LABEL_STORE;
import static com.hardmatch.checker.interfaces.InterfaceStore.STORE_NAME;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;

import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.apache.commons.logging.impl.SimpleLog;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;
import org.jdom.output.Format;
import org.jdom.output.XMLOutputter;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.checker.components.ComponentFactory;
import com.hardmatch.checker.components.IComponent;
import com.hardmatch.checker.components.ComponentFactory.UnknownComponentException;
import com.sirolf2009.util.neo4j.NeoUtil;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Checker {

	public static String NEO4J_FINAL_IP = "http://localhost";
	//public static int NEO4J_FINAL_PORT = 7474;
	public static String NEO4J_TEMP_IP = "http://localhost";
	public static int NEO4J_TEMP_PORT = 7484;
	public static boolean SHOULD_CONNECT = false;
	public static String SERVER_PORT_FILE_LOC = "/usr/local/bin/HardMatch/neo4JPort.xml";
	public static SimpleLog log = new SimpleLog("checker");

	public RestAPI restTemp;
	public RestAPI restFinal;


	public Checker(Options options, String[] args) {
		initFromCommandLine(options, args);
		run();
	}

	public Checker() {
		initFromProperties();
		run();
	}

	public void run() {
		restFinal.sendCypher("MATCH ()-[r]-() DELETE r");
		restFinal.sendCypher("MATCH (n) DELETE n");
		transferDB();
		check();
	}

	public void transferDB() {
		JSONObject components = restTemp.sendCypher("MATCH (n:Component) RETURN n, labels(n), id(n)");
		List<JSONArray> rows = restTemp.json.getRowsFromQuery(components);
		log.info("Copying over "+rows.size()+" nodes");
		for(int i = 0; i < rows.size(); i++) {
			JSONArray row = rows.get(i);
			try {
				IComponent component = ComponentFactory.getComponent((JSONObject) row.get(0), row.get(1).toString(), (Long)row.get(2));
				URI node = getOrCreateNode(component);
				//System.out.println(restTemp.relationship.getRelationships(restTemp.nodes.fromID((Long)row.get(2))));
				createStoreLinks(restTemp.relationship.getRelationships(restTemp.nodes.fromID(component.getID())), node);
			} catch (UnknownComponentException e) {
				e.printStackTrace();
			} catch (URISyntaxException e) {
				e.printStackTrace();
			}
		}
		log.info("done");
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

	public void check() {
		ComponentChecker setup = createSetup();
		setup.crossCheckAll();
	}

	public ComponentChecker createSetup() {
		ComponentChecker setup = new ComponentChecker(this);
		JSONObject components = restFinal.sendCypher("MATCH (n:Component) RETURN n, labels(n), id(n)");
		for(Object rowObject : restFinal.json.getRowsFromCypherQuery(components)) {
			JSONArray row = (JSONArray) rowObject;
			try {
				setup.addComponentToSetup(ComponentFactory.getComponent((JSONObject) row.get(0), row.get(1).toString(), (Long)row.get(2)));
			} catch (UnknownComponentException e) {
			}
		}
		return setup;
	}

	public void initFromCommandLine(Options options, String[] args) {
		CommandLineParser parser = new BasicParser();
		try {
			CommandLine cmd = parser.parse(options, args);
			if(cmd.hasOption("hf")) {
				NEO4J_FINAL_IP = cmd.getOptionValue("hf");
			}
			if(cmd.hasOption("ht")) {
				NEO4J_TEMP_IP = cmd.getOptionValue("hf");
			}
			if(cmd.hasOption("pt")) {
				try {
					NEO4J_TEMP_PORT = Integer.parseInt(cmd.getOptionValue("pt"));
				} catch (NumberFormatException e) {
					log.fatal(cmd.getOptionValue("pf") + " is not a valid number. Exiting...", e);
					System.exit(1);
				}
			}
			if(cmd.hasOption("d")) {
				SHOULD_CONNECT = true;
			}
			if(cmd.hasOption("x")) {
				SERVER_PORT_FILE_LOC = cmd.getOptionValue("x");
			}
		} catch(ParseException e) {
			e.printStackTrace();
		} catch(NumberFormatException e) {
			e.printStackTrace();
		}
		init();
	}

	public void initFromProperties() {
		try {
			File file = new File("properties");
			if(!file.exists()) {
				log.info("Writing new properties file to "+file.getAbsolutePath());
				file.createNewFile();
			}
			PropertiesConfiguration config = new PropertiesConfiguration("properties");
			if(config.containsKey("hf")) {
				NEO4J_FINAL_IP = config.getString("hf");
			} else {
				config.addProperty("hf", NEO4J_FINAL_IP);
			}
			if(config.containsKey("ht")) {
				NEO4J_FINAL_IP = config.getString("hf");
			} else {
				config.addProperty("ht", NEO4J_FINAL_IP);
			}
			if(config.containsKey("d")) {
				SHOULD_CONNECT = config.getBoolean("d");
			} else {
				config.addProperty("d", SHOULD_CONNECT);
			}
			if(config.containsKey("x")) {
				SERVER_PORT_FILE_LOC = config.getString("x");
			} else {
				config.addProperty("x", SERVER_PORT_FILE_LOC);
			}
			config.save();
		} catch (ConfigurationException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		init();
	}

	private void init() {
		try {
			log.info("Setting Neo4J Temp root to "+NEO4J_TEMP_IP+":"+NEO4J_TEMP_PORT+"/db/data/");
			restTemp = new RestAPI(new URI(NEO4J_TEMP_IP)+":"+NEO4J_TEMP_PORT+"/db/data/");
			NeoUtil.log.setLevel(SimpleLog.LOG_LEVEL_OFF);
		} catch (URISyntaxException e) {
			log.fatal(NEO4J_TEMP_IP+":"+NEO4J_TEMP_PORT+" is not a valid URI", e);
			System.exit(-2);
		}
		SAXBuilder builder = new SAXBuilder();
		Element element = new Element("port").setText("UNDEFINED");
		try {
			File file = new File(SERVER_PORT_FILE_LOC);
			if(!file.exists()) {
				file.createNewFile();
			}
			Document document = (Document) builder.build(file);
			element = document.getRootElement().getChild("port");
			if(element == null) {
				element = new Element("port").setText("7474");
				document.addContent(element);
				XMLOutputter xmlOutput = new XMLOutputter();
				xmlOutput.setFormat(Format.getPrettyFormat());
				xmlOutput.output(document, new FileWriter(SERVER_PORT_FILE_LOC));
			}
			log.info("Setting Neo4J Final root to "+NEO4J_FINAL_IP+":"+Integer.parseInt(element.getText())+"/db/data/");
			restFinal = new RestAPI(new URI(NEO4J_FINAL_IP+":"+Integer.parseInt(element.getText())+"/db/data/"));
		} catch (JDOMException e) {
			log.fatal(SERVER_PORT_FILE_LOC+" is not an XML file", e);
			System.exit(-3);
		} catch (IOException e) {
			log.fatal(SERVER_PORT_FILE_LOC+" could not be read", e);
			System.exit(-4);
		} catch (URISyntaxException e) {
			log.fatal(NEO4J_FINAL_IP+":"+element.getText()+"/db/data/ is not a valid URI", e);
			System.exit(-4);
		}
		changePortsInXML();
		new SynonymChecker();
		if(SHOULD_CONNECT) {
			new Thread(new Runnable() {
				@Override
				public void run() {
					new NetworkManagerChecker();
				}
			}).start();
			log.info("Initialized. Checking now");
		}
	}

	public void changePortsInXML() {
		try {
			SAXBuilder builder = new SAXBuilder();
			Document document = (Document) builder.build(new File(SERVER_PORT_FILE_LOC));
			Element element = document.getRootElement().getChild("port");
			if(element.getText().equals("7474")) {
				element.setText("7494");
			} else {
				element.setText("7474");
			}
			XMLOutputter xmlOutput = new XMLOutputter();
			xmlOutput.setFormat(Format.getPrettyFormat());
			xmlOutput.output(document, new FileWriter(SERVER_PORT_FILE_LOC));
		} catch (JDOMException | IOException e) {
			log.error("An error occured during changing the ports file", e);
		}
	}

	public static void main(String[] args) {
		if(args.length > 0) {
			log.info("Running checker from command line parameters");
			Options options = new Options();
			options.addOption("hf", true, "Default: \"http://localhost\". The IP address of the final Neo4J");
			options.addOption("ht", true, "Default: \"http://localhost\". The IP address of the temporary Neo4J");
			options.addOption("pt", true, "Default: 7484. The port of the temporary Neo4J");
			options.addOption("d", false, "Default: false. Determines if the checker should connect to the java dashboard");
			options.addOption("x", true, "Default: /usr/local/bin/HardMatch/neo4JPort.xml. The location of the file to write/read the most updated DB port");
			new Checker(options, args);
		} else {
			new Checker();
		}
	}
}
