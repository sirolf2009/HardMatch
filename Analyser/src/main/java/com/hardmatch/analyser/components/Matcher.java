package com.hardmatch.analyser.components;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class Matcher implements IComponent {
	
	private double amount;
	
	private double workingTime;
	private double compatibleSetups;
	
	public void handleMetaDataObject(DBObject object) {
		double timeMatcherStarted = Long.parseLong(object.get("TimeMatcherStarted").toString());
		double timeMatcherEnded = Long.parseLong(object.get("TimeMatcherEnded").toString());
		workingTime += timeMatcherEnded - timeMatcherStarted;
		boolean compatible = Boolean.parseBoolean(object.get("CompatibleSetup").toString());
		if(compatible) {
			compatibleSetups++;
		}
		amount++;
	}

	public void finalize(DBObject root) {
		BasicDBObject doc = new BasicDBObject();
		doc.append("AvgCalculationTime", workingTime/amount);
		doc.append("RequestsPerMinute", (workingTime/amount)/1000/60);
		double ratio = 1/(double)amount;
		ratio *= compatibleSetups;
		doc.append("CompatibleSetupRatio", ratio);
		root.put("MatcherMetadata", doc);
	}

}
