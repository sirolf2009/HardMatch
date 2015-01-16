#!/bin/bash
python3 clearTempDb.py
cd Crawler
python3 InformatiqueCrawlerV3.py
cd ..
cd checker
sudo mvn exec:java -Dexec.mainClass="com.hardmatch.checker.Checker"
