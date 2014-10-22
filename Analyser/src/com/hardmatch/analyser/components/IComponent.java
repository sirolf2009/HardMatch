package com.hardmatch.analyser.components;

import com.mongodb.DBObject;

public interface IComponent {
	
	public void handleMetaDataObject(DBObject object);
	public DBObject getAnalysedData();

}
