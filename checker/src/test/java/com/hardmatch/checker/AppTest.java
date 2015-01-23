package com.hardmatch.checker;

import org.junit.Assert;
import org.junit.Test;

import com.hardmatch.checker.components.ComponentCase;

public class AppTest {
	
	@Test
	public void testSynonymChecker() {
		SynonymChecker checker = new SynonymChecker();
		Assert.assertEquals(true, checker.areEqual("PCIe", "PCI-e"));
		Assert.assertEquals(true, checker.areEqual("SATA", "Serieel ATA"));
		Assert.assertEquals(false, checker.areEqual("PCIe", "SATA"));
		Assert.assertEquals(true, checker.areEqual("NULL", "SATA"));
		Assert.assertEquals(true, checker.areEqual("AM1", "AM1"));
		
		Assert.assertArrayEquals(new String[] {"Micro ITX"}, new String("Micro ITX").split(", "));
	}

} 
