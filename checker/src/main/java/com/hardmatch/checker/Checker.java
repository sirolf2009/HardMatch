package com.hardmatch.checker;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.apache.commons.logging.impl.SimpleLog;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.checker.components.ComponentFactory;
import com.hardmatch.checker.components.ComponentFactory.UnknownComponentException;
import com.sirolf2009.util.neo4j.NeoUtil;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Checker {

	public static String NEO4J_FINAL_IP = "http://localhost";
	public static int NEO4J_FINAL_PORT = 7474;
	public static String NEO4J_TEMP_IP = "http://localhost";
	public static int NEO4J_TEMP_PORT = 7484;
	public static int THRIFT_PORT = 9091;
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
		check();
	}
	
	public void check() {
		ComponentChecker setup = createSetup();
		setup.crossCheckAll();
	}

	public ComponentChecker createSetup() {
		ComponentChecker setup = new ComponentChecker(this);
		JSONObject components = restTemp.sendCypher("MATCH (n:Component) RETURN n, labels(n), id(n)");
		for(Object rowObject : restTemp.json.getRowsFromCypherQuery(components)) {
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
			if(cmd.hasOption("h")) {
				NEO4J_FINAL_IP = cmd.getOptionValue("h");
			}
			if(cmd.hasOption("p")) {
				NEO4J_FINAL_PORT = Integer.parseInt(cmd.getOptionValue("p"));
			}
			if(cmd.hasOption("t")) {
				THRIFT_PORT = Integer.parseInt(cmd.getOptionValue("t"));
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
			if(config.containsKey("pf")) {
				NEO4J_FINAL_PORT = config.getInt("pf");
			} else {
				config.addProperty("pf", NEO4J_FINAL_PORT);
			}
			if(config.containsKey("ht")) {
				NEO4J_FINAL_IP = config.getString("hf");
			} else {
				config.addProperty("ht", NEO4J_FINAL_IP);
			}
			if(config.containsKey("pt")) {
				NEO4J_FINAL_PORT = config.getInt("pf");
			} else {
				config.addProperty("pt", NEO4J_FINAL_PORT);
			}
			if(config.containsKey("t")) {
				THRIFT_PORT = config.getInt("t");
			} else {
				config.addProperty("t", THRIFT_PORT);
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
			log.info("Setting Neo4J root to "+NEO4J_FINAL_IP+":"+NEO4J_FINAL_PORT+"/db/data/");
			restFinal = new RestAPI(new URI(NEO4J_FINAL_IP+":"+NEO4J_FINAL_PORT+"/db/data/"));
			restTemp = new RestAPI(new URI(NEO4J_TEMP_IP)+":"+NEO4J_TEMP_PORT+"/db/data/");
			NeoUtil.log.setLevel(SimpleLog.LOG_LEVEL_OFF);
		} catch (URISyntaxException e) {
			log.error(NEO4J_FINAL_IP+":"+NEO4J_FINAL_PORT+" is not a valid URI");
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		if(args.length > 0) {
			Options options = new Options();
			options.addOption("hf", true, "Default: \"http://localhost\". The IP address of the final Neo4J");
			options.addOption("pf", true, "Default: 7474. The port of the final Neo4J");
			options.addOption("ht", true, "Default: \"http://localhost\". The IP address of the temporary Neo4J");
			options.addOption("pt", true, "Default: 7474. The port of the temporary Neo4J");
			options.addOption("t", true, "Default: 9091. The port to host on Thrift");
			new Checker(options, args);
		} else {
			new Checker();
		}
	}

}
