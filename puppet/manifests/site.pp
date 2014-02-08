node 'default' {
	include developer_keys
	include git
	include motd
}

node 'webserver' inherits default{
	include oracle_java
	include python_ai
    include pip
}

node 'database' inherits webserver{
	include couchdb
}
# Note the quotes around the name! Node names can have characters that
      # aren't legal for class names, so you can't always use bare, unquoted
      # strings like we do with classes.
node 'fountin','fountin2', 'jeff-test' inherits database{
    }

node 'fountin-design' inherits webserver{
	
}