class python_ai {
    package{'libspatialindex-dev':
    	name => "libspatialindex-dev",
    	ensure => latest,
    }
    package{'libgeos-dev':
    	name => "libgeos-dev",
    	ensure => latest,
    }
    
	pip::lib {
	    'bottle':
	        ensure	=> latest,
    }pip::lib {
         'numpy':
	        ensure	=> latest,
    }pip::lib {
		'pyproj':
	        ensure	=> latest,    
    }pip::lib {    
	    'rtree':
	    	ensure	=> latest,
	}pip::lib {
	    'couchdb':
	    	ensure	=> latest,
	}pip::lib {
	    'twython':
	        ensure	=> '1.3.4';
	}
}
