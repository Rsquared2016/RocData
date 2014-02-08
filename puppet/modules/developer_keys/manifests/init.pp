class developer_keys {
	#add the deploy keys for the specific servers
	file {
        "/root/.ssh/":
        path    => "/root/.ssh/",
        ensure  => directory,
        mode    => 700,
        owner   => root,
        group   => root;
        "/root/.ssh/authorized_keys":
        path    => "/root/.ssh/authorized_keys",
        mode    => 600,
        owner   => root,
        group   => root;
        "/root/.ssh/id_rsa":
		  owner => root,
		  group => root,
		  mode  => 600,
		  content => "-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----";
	"/root/.ssh/id_rsa.pub":
		  owner => root,
		  group => root,
		  mode  => 644,
		  content => "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQD0AoZoHre9qikFFJP5ejH/qT7C33JfwvkJ3OzTRBqI5ETyLMfRuQpNKcTxPgQOalFeKoyTWSE7npC0syh+8iJT5S5a1637zSrjITqNYd+rtBstq8hC8BOJhafj9in5Un0032/jDkWU7QIZ2knfjM+Tvp1cB12oTjgcEwH6lJQOtWR30LKRi9d7FvDjdvFVbpqiHaQFfM88AkkrUfMIdu6sArJIClKyC4q/8aL8yvmH+YaZIrr8jGiDSfgYJga3U+jiuYZ88zpUi+mYFN6K5Zt5Octo0V0AVyBTLIZTfJBUF8X4CmnNJwSHX3LQlXydQn3JklEFsp7p47XpNpqD3Dfa9rqhsvf9l02Ae9yWowZHIKq3NHISPpZdHi9fgFTq+6ZahN+Rh0qjnBPRHfCPrdCinzTaCxm2aZPR9+ABvyzhml/JBeHkGYlZqXNutHENoWgS6Nbc5XHAoc2D/1X4gVtWa+7I5NOcPwUUP94vtt7S6DrT1RbIylqKJbgdqE3FyNaHwzXIF8t5b/HnK5x5TUuKarEoOzKTy3BoFWEL2nGjdzvaxx6IIA5ECtiLrOS41PoJFBfxCPupfNXIHNZ1M2O1EOizK8Bw7DRPWOE4VhrsdBlQl4GuLOo0IwnlFq7y1jwpjlJa6T/xa9WxfK1Aaz4ebbAJx69/1TOj6wiFhSRmkQ== root@fountin";
     }
     
    ssh_authorized_key{
	 'androwis@fount.in':
	        user => 'root',
	        ensure => present,
	        key => "AAAAB3NzaC1yc2EAAAABIwAAAQEAy1pxt7Sa7KlCsyTkE+BT3uqplNMCqSxJcE+dhfei4195FmVOig2OMGjtH86d/QcWAM9DRXmIlFhBohsU2s8lFB5fT6WjGKx3OcYbR4Extuq9Vw61O1b41j5uFF66yLjytssDidB9AURt/EXtEZ22ureEIFqzNL8AUkPM5Xd2MMTODWOxpbcX61lkWpwlHmHYsZolI0MnrLLaCG5Kg/WIGXD7izIqgUlclQzaG/ZG9P7dp6vmTG8y4Eu/la56pp1KPMWcx1mi5QYry9CoGYajhpNNBoHQldRUvDQgJIjbStdex9Moh55jrXqYHkHPVOZehfBcOy+yw9lzXV4H0T34zw==",
	        target => '/root/.ssh/authorized_keys',
	        type => 'ssh-rsa';
	 'sean.brennan@fount.in':
		user => 'root',
		ensure => present,
	    key => "AAAAB3NzaC1yc2EAAAADAQABAAABAQC29ZiBl9/TU/5HAX8E8q4E/JJ9De3BogVa3ByQeunkCklnp27zd3292ZNHlC0dkLOq4fJ87Sq2jRPlrJR46X64TlqE1fGAk5EZRJ28pJYMYjJX3jHB2PUgrle2rtJgE0xqE2Hv1F4JcKZ4oQmWiysQdALq74Yp/1UsaDCLG3i96sYpZ9IPvyvtEJjHolkQsPG8fYRW5cyhRAVIJDpwtSIMto/smpHdiFFkqxCXhq6VV8dgjNSWySl5NLjm/zXtpUzN0KSkW0rpeuOWMnuUqTjeL3XtoKU+g9Nt9oY3C9NwmWXrW86xSYEgoP+WZE7+YNaxlf++CyQk8LtWfXQpqgot",
	    target => '/root/.ssh/authorized_keys',
	    type => "ssh-rsa";
	 'martin.janda@fount.in':
		user => 'root',
		ensure => present,
	        key => "AAAAB3NzaC1yc2EAAAADAQABAAABAQDKmJApbRnvKvq696f8m2saY0EfxNSuxpf0/zV2xsQHqSDQXXQc9t57zkVEIMc/wNBAclKv/x8sdBVsjMyar4CBfKlnTsbCK/fkh6Nc/hS6NmxGusLjsDu4NIdy9CwkSEbyJ12mZM9nG3mCUR4NdGOpbOYfXfBIg+Wa4aaX/uNkAXs+PlDLIk0wYUy2qRmQo0BpUNMG5c3pCfK+zBKd/AadimQyOc8rQVZfAWj5zHOrS9jk7+R0Mu0fjdCPo65nNPdMO7bvoQ+ZoOuX0G4/52Lx73u6mUGcpauDfacP5k5QIuCiTS/MZCVeepZ+ekQNf26+bjg44tQIOqzghfNhc7jJ",
	        target => '/root/.ssh/authorized_keys',
	        type => "ssh-rsa";
	'adam@adam.local':
		user => 'root',
		ensure => present,
	        key => "AAAAB3NzaC1kc3MAAACBAP06vA2Irwla1hD+Ry5+4vftiLwQWtQ2JKBUboGP7fObxsgKddupRBCN/tZCkH66T4M9Wu4/phnVET6Gl+ElVXQpVMSvilIdVDiHEKkdR0NiQCESXQSD+klHp8XiX2oE9GJcL9pw9xzCydj2MMgs1BhCfiH3E6nzC8gJXTKuqE2/AAAAFQDIpybav8PymN6xjwNpmkg5reKsnQAAAIBFADTcrZrHHeuFJ5z5YUuY88gjvzZe2kQsY4vcV4MlCf+miW2lOtOeHPASQan7wh1PD9tgsQcjbyDKIFX6oo69VZ7kbBIQ/FRqcVQjuFv2jODwQK1bHPLt3Di/YI4Pgzu47hFdFlfGCwbl7LaXhGIbbTdK2bZ5ah96+qgzJ5+LkQAAAIEA2ZfkQPNNys2IGn794g5yEqfslCmNnrQ0mqowJiTOC0Wf8v8g+zXkQz7h2Mbn24HpX3N8dD6BkRcHeQ4OCUz8o5/cR7PIPDLa31ruy2EIMojgOyQrsIhj2LuJgCrR5bSJYbN7HHTIvEEov60OjnKdrXG1pLJ6Gj0B4idCCEw/ItA=",
	        target => '/root/.ssh/authorized_keys',
	        type => "ssh-dss";
	  'adam@fount.in':
		user => 'root',
		ensure => present,
	        key => "AAAAB3NzaC1kc3MAAACBAMzaGGvpOdi6+8Izw68Ao8gOdtBFzOx2QZht4aH2d9Nu0rWpDz/sRJbUw/85mYTUnzxlFE9wB1nLdluY/GiCjyBEvdqS0yeNkUvXcNOZ7nJvclrtZ8HjvnCKxceaC0RKSOJNWneyz66wLA0Nq881XRDP4H3qMLkkRyBzu6LU6CpVAAAAFQCDNLBLu1/+5gGBjypYu+pikg5qjwAAAIB+W+e0Fq++ETeroq9/nUdPuRfc9YMi3HonlIPhk4hYIKUzsyfXGi4+Xjpi2CbC4hDa9phdftIuxKzNxPYeyKw/N7P1KrNOVvDAnafvXLFsevgrIvdTwD+YL2iHtxrPylQeZNZNwEQTjOUiOlgKAmxY8IAnK2sP6A3maW2FMG19UAAAAIArAboeZriP+diQzYpuUYt+0LnKFL1d0P8JFCTb+ibVoCaJQcN5a+7L82+HPCp2Z6kwQpsAmyJ0IExwe+jzjHAX0lMTWkRV/xzX3r1BAiMBHsS2kIt/bBDzcLakN5+sJuNpEJ4VDyrPP1RPrXmoIIp0iz5tuw0B3360OpccjWoOWA==",
	        target => '/root/.ssh/authorized_keys',
	        type => "ssh-dss",
	}
}