# cfengine_stuffs
Random CFEngine test promises written for my home lab

## Contents
1. *my_autofs.cf*     => Policy for autofs, used for auto mounting of user home dir
2. *my_dns.cf*        => Policy to configure master name server using bind
3. *my_user.cf*       => Automates local user creation as well as adding sudo privilege
4. *my_ssh.cf*        => Configures SSH service with "UseDNS no"
5. *my_package.cf*    => Basic packages required for troubleshooting etc.
6. *my_repo.cf*       => Configures yum repositories
7. *my_freespace.cf*  => Checks and alerts for free spaces in /, /var, /tmp on an hourly basis
8. *my_services.cf*   => Policy to have a check on the basic services
9. *my_test.cf*       => Random test policy
10. *my_env.cf*       => Test policy for maintaining an updated Ruby environment
11. *my_update_cfe.cf*=> Updates CFEngine automatically to the latest version (without much hassle)
12. *my_resolv.cf*  => Builds /etc/resolv.conf
13. *my_log.cf*       => Changes permission on various log files so normal users can read them
14. *my_ntp.cf*       => Configures ntpd and timezone, uses mustache template to produce the ntp.conf file
15. *my_database.cf*  => Installs mysql-server and creates a sample DB and Table
16. *my_motd.cf*      => Creates /etc/motd from a mustache template with verbose host information
