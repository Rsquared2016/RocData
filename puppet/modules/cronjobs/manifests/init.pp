class cronjobs{
	
	file {
	## This is a sample cronjob to be scheduled on a machine.
	"dbdump.cron":
    	path    => "/etc/cron.d/dbdump.cron",
    	ensure  => present,
    	owner   => "root",
    	group   => "root",
    	mode    => 0644,
    	require => [
                Package["mysql-server"],
                Service["mysqld"]
               ],
    	content => "0 0 * * * root /usr/local/sbin/dbdump\n";  #trailing '\n' is required.
	}
}