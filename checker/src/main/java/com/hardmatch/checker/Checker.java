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
	public static boolean SHOULD_CONNECT = false;
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
			if(cmd.hasOption("hf")) {
				NEO4J_FINAL_IP = cmd.getOptionValue("hf");
				log.info("setting ");
			}
			if(cmd.hasOption("pf")) {
				NEO4J_FINAL_PORT = Integer.parseInt(cmd.getOptionValue("pf"));
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
			if(config.containsKey("d")) {
				SHOULD_CONNECT = config.getBoolean("d");
			} else {
				config.addProperty("d", SHOULD_CONNECT);
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
			log.info("Setting Neo4J Final root to "+NEO4J_FINAL_IP+":"+NEO4J_FINAL_PORT+"/db/data/");
			log.info("Setting Neo4J Temp root to "+NEO4J_TEMP_IP+":"+NEO4J_TEMP_PORT+"/db/data/");
			restFinal = new RestAPI(new URI(NEO4J_FINAL_IP+":"+NEO4J_FINAL_PORT+"/db/data/"));
			restTemp = new RestAPI(new URI(NEO4J_TEMP_IP)+":"+NEO4J_TEMP_PORT+"/db/data/");
			NeoUtil.log.setLevel(SimpleLog.LOG_LEVEL_OFF);
		} catch (URISyntaxException e) {
			log.error(NEO4J_FINAL_IP+":"+NEO4J_FINAL_PORT+" is not a valid URI");
			e.printStackTrace();
		}
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

	public static void main(String[] args) {
		if(args.length > 0) {
			log.info("Running checker from command line parameters");
			Options options = new Options();
			options.addOption("hf", true, "Default: \"http://localhost\". The IP address of the final Neo4J");
			options.addOption("pf", true, "Default: 7474. The port of the final Neo4J");
			options.addOption("ht", true, "Default: \"http://localhost\". The IP address of the temporary Neo4J");
			options.addOption("pt", true, "Default: 7484. The port of the temporary Neo4J");
			options.addOption("d", false, "Default: false. Determines if the checker should connect to the java dashboard");
			new Checker(options, args);
		} else {
			new Checker();
		}
	}
}
