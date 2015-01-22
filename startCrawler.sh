#!/bin/bash

while true; do

	echo "Clearing DB"
	python3 clearTempDb.py
	echo "Starting informatique crawler"
	python3 Crawler/InformatiqueCrawlerV3.py
	echo "Starting Coolblue crawler"
	python3 Crawler/Coolblue.py

	echo "Starting checker"
	sudo mvn install exec:java -f checker/pom.xml -Dexec.mainClass="com.hardmatch.checker.Checker"

	sleep 3600*60*24

done
