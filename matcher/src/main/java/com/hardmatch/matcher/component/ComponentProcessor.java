package com.hardmatch.matcher.component;

public class ComponentProcessor extends Component {
	
	private String socketType;

	public ComponentProcessor() {
	}
	
	@Override
	public boolean isCompitableWith(Component component) {
		if(component instanceof ComponentMotherboard) {
			return ((ComponentMotherboard)component).getSocketType().equals(socketType);
		}
		return false;
	}

	public String getSocketType() {
		return socketType;
	}

	public void setSocketType(String socketType) {
		this.socketType = socketType;
	}

}
