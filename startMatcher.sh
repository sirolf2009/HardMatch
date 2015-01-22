#!/bin/bash
sudo mvn -f matcher/pom.xml clean install exec:java -Dexec.mainClass="com.hardmatch.matcher.ThriftServerMatcher"

