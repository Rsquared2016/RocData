#!/bin/bash
mvn jetty:stop clean install jetty:run -Denvironment=development -DlogbackConfigLocation=classpath:logback-development.xml &
echo "webapp running"
