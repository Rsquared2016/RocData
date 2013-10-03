#!/bin/bash
mvn jetty:stop clean install jetty:run -DlogbackConfigLocation=classpath:logback-production.xml -Denvironment=production &
echo "webapp running"
