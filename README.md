# cfengine_stuffs
Random CFEngine test promises written for my home lab

This branch is for testing CFEngine 3.7.x

Added an OpenLDAP based External Node Classification module. Take a look at promise.cf to know how I raise classes based on node's roles.

__extract_raise_classes__ => uses query-enc.py to query LDAP server for roles of the host node. (To be run once in 25-30 mins, due to it's being costly in execution), it then writes to /etc/cfe.d/roles_classes with classes following CFEngine's module protocol. At any time, if it fails to query LDAP, the old /etc/roles_classes is kept as it is.

__raise_classes__ => It just cat's /etc/roles_classes. This is done during every cf-agent run of course.

__Mustache Template__ => my_repo.cf, my_ntp.cf, my_resolv_conf.cf etc. promises make use of the new Mustache Templates. It's awesome and easy!!

## Contents
1. `my_autofs.cf`     => Policy for autofs, used for auto mounting of user home dir
2. `my_dns.cf`        => Policy to configure master name server using bind
3. `my_user.cf`       => Automates local user creation as well as adding sudo privilege
4. `my_ssh.cf`        => Configures SSH service with "UseDNS no"
5. `my_package.cf`    => Basic packages required for troubleshooting etc.
6. `my_repo.cf`       => Configures yum repositories
7. `my_freespace.cf`  => Checks and alerts for free spaces in /, /var, /tmp on an hourly basis
8. `my_services.cf`   => Policy to have a check on the basic services
9. `my_test.cf`       => Random test policy
10. `my_env.cf`       => Test policy for maintaining an updated Ruby environment
11. `my_update_cfe.cf`=> Updates CFEngine automatically to the latest version (without much hassle)
12. `my_resolv.cf`  => Builds /etc/resolv.conf
13. `my_log.cf`       => Changes permission on various log files so normal users can read them
14. `my_ntp.cf`       => Configures ntpd and timezone, uses mustache template to produce the ntp.conf file
15. `my_database.cf`  => Installs mysql-server and creates a sample DB and Table
16. `my_motd.cf`      => Creates /etc/motd from a mustache template with verbose host information
17. `my_monitoring.cf`      => Zabbix monitoring agent configuration
18. `my_docker.cf`      => Docker configuration policy
19. `my_managee_mps.cf`      => Manages master policy server, right now it installs and configures OpenLDAP based External Node Classifier system
... and many more
