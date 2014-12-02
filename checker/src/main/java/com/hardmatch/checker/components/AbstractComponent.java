package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public abstract class AbstractComponent implements IComponent {
	
	private Long ID;
	private String labels;
	private String modelID;

	public AbstractComponent(String labels, Long ID) {
		this.labels = labels;
		this.ID = ID;
	}

	public boolean isCompatibleWith(IComponent other) {
		return false;
	}

	public void populateProperties(JSONObject object) {
		modelID = object.get(MODEL_ID).toString();
	}
	
	public String getModelID() {
		return modelID;
	}

	public long getID() {
		return ID;
	}

	public String getLabels() {
		return labels;
	}

	public static String MODEL_ID = "modelID";
	public static String SOCKET_LABEL = "socket";

}
