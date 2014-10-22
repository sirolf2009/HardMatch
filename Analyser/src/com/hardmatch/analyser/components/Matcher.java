package com.hardmatch.analyser.components;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class Matcher implements IComponent {
	
	private long amount;
	
	private long workingTime;
	private long compatibleSetups;
	
	public void handleMetaDataObject(DBObject object) {
		long timeMatcherStarted = Long.parseLong(object.get("TimeMatcherStarted").toString());
		long timeMatcherEnded = Long.parseLong(object.get("TimeMatcherEnded").toString());
		workingTime += timeMatcherStarted - timeMatcherEnded;
		boolean compatible = Boolean.parseBoolean(object.get("CompatibleSetup").toString());
		if(compatible) {
			compatibleSetups++;
		}
		amount++;
	}

	public DBObject getAnalysedData() {
		BasicDBObject doc = new BasicDBObject("Matcher", "value?");
		doc.append("AvgCalculationTime", workingTime/amount);
		doc.append("RequestsPerMinute", (workingTime/amount)/amount*1000);
		doc.append("CompatibleSetupRatio", 1/(amount)*compatibleSetups);
		return doc;
	}

}
