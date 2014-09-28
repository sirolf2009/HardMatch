package com.hardmatch.matcher.component;

public class ComponentMotherboard extends Component {
	
	private String socketType;

	public ComponentMotherboard() {
		setComponentType(ComponentType.MOTHERBOARD);
	}
	
	@Override
	public boolean isCompitableWith(Component component) {
		if(component instanceof ComponentProcessor) {
			return ((ComponentProcessor)component).getSocketType().equals(socketType);
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
