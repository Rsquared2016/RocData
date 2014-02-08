class oracle_java {
	package {
		'maven':
	      name   => "maven",
	      ensure => latest;
		'openjdk*':
			ensure => absent;
      }
	
	
	$java_distrib='jdk'
	$java_version='7u7'  
$arch = $architecture ? {
    'amd64' => 'x64',
    default => 'i586',
  }
  $package_name = "${java_distrib}-${java_version}-linux-${arch}.gz"
  file { '/usr/local/java':
    ensure => directory,
  }
  file { "/usr/local/java/${package_name}":
    ensure  => present,
    source  => "puppet:///modules/oracle_java/${package_name}",
    require => File['/usr/local/java'],
    notify  => Exec['unpack-java'],
  }
  exec { 'unpack-java':
    command     => "tar zxf ${package_name}",
    cwd         => '/usr/local/java/',
    path        => '/bin',
    refreshonly => true,
    notify      => Exec['rename-java-dir'],
  }
  exec { 'rename-java-dir':
    command     => "mv jdk1.* ${java_version}",
    cwd         => '/usr/local/java/',
    path        => '/usr/lib/jvm/',
    refreshonly => true,
    notify		=> Exec['update-alt0'],
  }
  exec { 'update-alt0':
    command     => 'update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.7.0_07/bin/java" 1',
    refreshonly => true,
    notify		=> Exec['update-alt1'],
  }
  exec { 'update-alt1':
    command     => 'update-alternatives --install "/usr/bin/javca" "javac" "/usr/lib/jvm/jdk1.7.0_07/bin/javac" 1',
    refreshonly => true,
  }
}
