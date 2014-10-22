package com.hardmatch.analyser.components;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class Crawler implements IComponent {
	
	private long amount;
	
	private long workingTime;
	private long errorCount;
	
	public void handleMetaDataObject(DBObject object) {
		workingTime += Long.parseLong(object.get("duration").toString());
		errorCount += Long.parseLong(object.get("errorcount").toString());
		amount++;
	}

	public DBObject getAnalysedData() {
		BasicDBObject doc = new BasicDBObject("Matcher", "value?");
		doc.append("AvgCalculationTime", workingTime/amount);
		doc.append("RequestsPerMinute", (workingTime/amount)/amount*1000);
		doc.append("ErrorRatio", 1/(amount)*errorCount);
		return doc;
	}

}
