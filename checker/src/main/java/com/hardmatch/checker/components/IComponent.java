package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public interface IComponent {
	
	public boolean isCompatibleWith(IComponent other);
	public void populateProperties(JSONObject object);
	public long getID();
	public String getModelID();
	public String getLabels();

}
