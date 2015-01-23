package com.hardmatch.checker;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.jdom.Document;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;

public class SynonymChecker {
	
	public List<List<String>> synonyms;
	
	public SynonymChecker() {
		this("src/rsc/synonyms.xml");
	}

	public SynonymChecker(String file) {
		this(new File(file));
	}
	
	public SynonymChecker(File file) {
		parse(file);
	}

	public void parse(String file) {
		parse(new File(file));
	}
	
	@SuppressWarnings("unchecked")
	public void parse(File file) {
		synonyms = new ArrayList<List<String>>();
		SAXBuilder builder = new SAXBuilder();
		try {
			Document document = (Document) builder.build(file);
			Element rootNode = document.getRootElement();
			addToSynonyms(rootNode.getChildren("SynonymList"));
		} catch (IOException io) {
			System.out.println(io.getMessage());
		} catch (JDOMException jdomex) {
			System.out.println(jdomex.getMessage());
		}
	}
	
	public void addToSynonyms(List<Element> elements) {
		for(Element element : elements) {
			synonyms.add(getList(element));
		}
	}
	
	public List<String> getList(Element element) {
		String delim = element.getAttributeValue("delimeter");
		String[] valueArray = element.getTextNormalize().split(delim == null ? "," : delim);
		return Arrays.asList(valueArray);
	}
	
	public boolean areEqual(String string1, String string2) {
		if(string1.equals("NULL") || string2.equals("NULL")) {
			return true;
		}
		if(string1.equalsIgnoreCase(string2)) {
			return true;
		}
		for(List<String> synonymList : synonyms) {
			if(synonymList.contains(string1) && synonymList.contains(string2)) {
				return true;
			}
		}
		return false;
	}

}
