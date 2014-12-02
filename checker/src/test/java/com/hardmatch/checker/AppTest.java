package com.hardmatch.checker;


import org.json.simple.JSONObject;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

import com.hardmatch.checker.components.ComponentCPU;
import com.hardmatch.checker.components.ComponentFactory;
import com.hardmatch.checker.components.ComponentMotherboard;

public class AppTest {

	public JSONObject i5CPU;
	public JSONObject i7CPU;
	public JSONObject msiMotherboard;
	
	@Before
	public void init() {
		i5CPU = new JSONObject();
		i5CPU.put(ComponentCPU.SOCKET_LABEL, "1150");
		i7CPU = new JSONObject();
		i7CPU.put(ComponentCPU.SOCKET_LABEL, "1155");
		
		msiMotherboard = new JSONObject();
		msiMotherboard.put(ComponentCPU.SOCKET_LABEL, "1150");
	}
	
	@Test
	public void testChecking() {
		try {
			ComponentCPU CPU1 = (ComponentCPU) ComponentFactory.getComponent(i5CPU, "Component, CPU", 0L);
			ComponentCPU CPU2 = (ComponentCPU) ComponentFactory.getComponent(i7CPU, "Component, CPU", 0L);
			ComponentMotherboard Motherboard1 = (ComponentMotherboard) ComponentFactory.getComponent(msiMotherboard, "Component, Motherboard", 0L);

			assertEquals("Component populate CPU", "1150", CPU1.socket);
			assertEquals("Component populate CPU", "1155", CPU2.socket);
			assertEquals("Component populate Motherboard", "1150", Motherboard1.socket);

			assertEquals("Compitability test", true, CPU1.isCompatibleWith(Motherboard1));
			assertEquals("Compitability test", true, Motherboard1.isCompatibleWith(CPU1));
			assertEquals("Compitability test", false, CPU2.isCompatibleWith(Motherboard1));
			assertEquals("Compitability test", false, Motherboard1.isCompatibleWith(CPU2));
			assertEquals("Compitability test", true, CPU2.isCompatibleWith(CPU1));
			assertEquals("Compitability test", true, CPU1.isCompatibleWith(CPU2));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

} 
