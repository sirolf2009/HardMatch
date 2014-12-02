package com.hardmatch.analyser;

import java.net.UnknownHostException;
import java.util.logging.Logger;

import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import com.hardmatch.analyser.components.Crawler;
import com.hardmatch.analyser.components.IComponent;
import com.hardmatch.analyser.components.Matcher;
import com.hardmatch.analyser.components.Website;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.Mongo;
import com.mongodb.MongoClient;

public class Analyser {

	public static String MONGODB_HOST = "localhost";
	public static int MONGODB_PORT = 27017;
	public static String MONGODB_DBNAME = "MetadataRaw";
	public static String MONGODB_METANAME_MATCHER = "MetadataRawMatcher";
	public static String MONGODB_METANAME_CRAWLER = "MetadataRawCrawler";
	public static String MONGODB_METANAME_WEBSITE = "MetadataRawWebsite";
	public static String MONGODB_METANAME_ANALYSED = "MetadataAnalysed";
	public static int sleepTime = 60000;
	
	public static Logger log = Logger.getLogger(Analyser.class.getName());
	
	private DB mongoDB;
	private DBCollection metadataMatcher;
	private DBCollection metadataCrawler;
	private DBCollection metadataWebsite;
	private DBCollection metadataAnalysed;
	private IComponent matcher;
	private IComponent crawler;
	private IComponent website;

	public Analyser(Options options, String[] args) {
		try {
			handleCLI(options, args);
			connectToDB();
			while(true) {
				retrieveRawMetadata();
				analyseRawMetadata();
				storeAnalysedMetadata();
			}
		} catch (UnknownHostException e) {
			log.severe("Could not make a connection to "+MONGODB_HOST+":"+MONGODB_PORT);
			e.printStackTrace();
		}
	}

	public void storeAnalysedMetadata() {
		DBObject root = new BasicDBObject();
		matcher.finalize(root);
		crawler.finalize(root);
		website.finalize(root);
		metadataAnalysed.insert(root);
	}

	public void analyseRawMetadata() {
		log.finer("Analysing matcher data");
		matcher = new Matcher();
		for(DBObject object : metadataMatcher.getIndexInfo()) {
			matcher.handleMetaDataObject(object);
		}
		log.finer("Analysing crawler data");
		crawler = new Crawler();
		for(DBObject object : metadataCrawler.find()) {
			crawler.handleMetaDataObject(object);
		}
		log.finer("Analysing website data");
		website = new Website();
		for(DBObject object : metadataWebsite.getIndexInfo()) {
			website.handleMetaDataObject(object);
		}
	}

	public void retrieveRawMetadata() {
		log.finer("Retrieving matcher metadata");
		metadataMatcher = mongoDB.getCollection(MONGODB_METANAME_MATCHER);
		log.finer("Retrieving crawler metadata");
		metadataCrawler = mongoDB.getCollection(MONGODB_METANAME_CRAWLER);
		log.finer("Retrieving website metadata");
		metadataWebsite = mongoDB.getCollection(MONGODB_METANAME_WEBSITE);
	}

	public void connectToDB() throws UnknownHostException {
		log.fine("Connecting to "+MONGODB_HOST+":"+MONGODB_PORT);
		Mongo mongoDBConnection = new MongoClient(MONGODB_HOST, MONGODB_PORT);
		log.fine("Selecting database "+MONGODB_DBNAME);
		mongoDB = mongoDBConnection.getDB(MONGODB_DBNAME);
		log.finer("Accessing analysed collection "+MONGODB_METANAME_ANALYSED);
		metadataAnalysed = mongoDB.getCollection(MONGODB_METANAME_ANALYSED);
	}

	public void handleCLI(Options options, String[] args) {
		CommandLineParser parser = new BasicParser();
		try {
			CommandLine cmd = parser.parse(options, args);
			if(cmd.hasOption("h")) {
				MONGODB_HOST = cmd.getOptionValue("h");
			}
			if(cmd.hasOption("p")) {
				MONGODB_PORT = Integer.parseInt(cmd.getOptionValue("p"));
			}
			if(cmd.hasOption("d")) {
				MONGODB_DBNAME = cmd.getOptionValue("d");
			}
			if(cmd.hasOption("cm")) {
				MONGODB_METANAME_MATCHER = cmd.getOptionValue("cm");
			}
			if(cmd.hasOption("cc")) {
				MONGODB_METANAME_CRAWLER = cmd.getOptionValue("cc");
			}
			if(cmd.hasOption("cw")) {
				MONGODB_METANAME_WEBSITE = cmd.getOptionValue("cw");
			}
			if(cmd.hasOption("s")) {
				sleepTime = Integer.parseInt(cmd.getOptionValue("s"));
			}
		} catch (ParseException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		Options options = new Options();
		options.addOption("h", true, "The IP of the host to connect to");
		options.addOption("p", true, "The port of the host to connect to");
		options.addOption("d", true, "The name of the database");
		options.addOption("cm", true, "The name of the collection of the raw metadata from the Matcher");
		options.addOption("cc", true, "The name of the collection of the raw metadata from the Crawler");
		options.addOption("cw", true, "The name of the collection of the raw metadata from the Website");
		options.addOption("ca", true, "The name of the collection of the analysed metadata");
		options.addOption("s", true, "The amount of miliseconds to sleep between every analysis");
		new Analyser(options, args);
	}

}
