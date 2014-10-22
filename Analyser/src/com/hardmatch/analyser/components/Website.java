package com.hardmatch.analyser.components;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class Website implements IComponent {
	
	private long amount;
	
	private long workingTime;
	private long registerdCount;
	
	public void handleMetaDataObject(DBObject object) {
		workingTime += Long.parseLong(object.get("duration").toString());
		if(Boolean.parseBoolean(object.get("Register").toString())) {
			registerdCount++;
		}
	}

	public DBObject getAnalysedData() {
		BasicDBObject doc = new BasicDBObject("Matcher", "value?");
		doc.append("AvgCalculationTime", workingTime/amount);
		doc.append("RequestsPerMinute", (workingTime/amount)/amount*1000);
		doc.append("RegisteredRatio", 1/(amount)*registerdCount);
		return doc;
	}

}
