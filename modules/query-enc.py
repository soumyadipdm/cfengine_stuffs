#!/usr/bin/python

import sys
import ldap
import argparse

class LdapEncException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class LdapEnc:
    def __init__(self, depth, ldaphost, basedn, user, password):
        self.range = {}
        self.basedn = basedn
        self.depth = depth
        self.result_arr = []

        if basedn not in user:
            user = "{0},{1}".format(user, basedn)

        self.groups_ou = "ou=groups,{0}".format(self.basedn)
        self.hosts_ou = "ou=hosts,{0}".format(self.basedn)

        try:
            self.ldap_conn = ldap.initialize("ldap://{0}:389/".format(ldaphost))
            self.ldap_conn.protocol_version = ldap.VERSION3
            self.ldap_conn.simple_bind_s(user, password)

        except ldap.LDAPError as e:
            raise LdapEncException(e)

    def _search_me(self, search_dn, memberof=True, depth=123456, hosts_only=False):
        if memberof:
            attr = 'memberOf'
        else:
            attr = 'member'


        try:
            result = self.ldap_conn.search_s(search_dn, ldap.SCOPE_SUBTREE, attrlist=[attr])

        except ldap.NO_SUCH_OBJECT:
            return self.result_arr

        except ldap.LDAPError as e:
            raise LdapEncException(e)

        if len(result):
            for t in result:
                if attr in t[1]:
                    for entry in t[1][attr]:

                        if depth >= 1:
                            entryname = entry.split(',')[0].split('cn=')[1]
                            depth = depth - 1

                            self._search_me(entry, memberof, depth)

                            if entryname != 'dummy-member-ignore':
                                if hosts_only and self.groups_ou in entry:
                                        continue

                                self.result_arr.append(entryname)


    def search(self, search_string):
        domain = self.basedn.replace("dc=", "").replace(",", ".")

        # memoberOf search
        if search_string.startswith("reverse:"):
            tmp_search_string = search_string.split("reverse:")[1]

            if domain in tmp_search_string:
                search_dn = "cn={0},{1}".format(tmp_search_string, self.hosts_ou)
                self._search_me(search_dn, memberof=True, depth=self.depth)
                if not len(self.result_arr):
                    self.result_arr.append("generic_host")

            else:
                search_dn = "cn={0},{1}".format(tmp_search_string, self.groups_ou)
                self._search_me(search_dn, memberof=True, depth=self.depth)

        # member search, but filter only to hosts
        elif search_string.startswith("hosts:"):
            tmp_search_string = search_string.split("hosts:")[1]

            if not domain in tmp_search_string:
                search_dn = "cn={0},{1}".format(tmp_search_string, self.groups_ou)
                self._search_me(search_dn, memberof=False, depth=self.depth, hosts_only=True)

            else:
                raise LdapEncException("hosts_search_is_applied_only_to_group")

        elif domain in search_string:
            # if forward lookup is doen on a host, it should throw exception
            raise LdapEncException("hosts_cannot_be_expanded")
            #search_dn = "cn={0},{1}".format(search_string, self.hosts_ou)
            #self._search_me(search_dn, memberof=False, depth=self.depth)

        # member search on a group
        else:
            search_dn = "cn={0},{1}".format(search_string, self.groups_ou)
            self._search_me(search_dn, memberof=False, depth=self.depth)

        return self.result_arr



## --- Main --- ##
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", "-d", type=int, default=123456789, help="depth of search e.g: 3, default: infinite")
    parser.add_argument("--file", "-f", help="write the result to a file")
    parser.add_argument("enc_query", help="query string e.g: reverse:host_name_fqdn (gives all groups that the host is a member of or hosts:group_name (gives all hosts that are in the group)")
    args = parser.parse_args()

    try:
        lr = LdapEnc(args.depth, "192.168.56.101", "dc=local,dc=net", "cn=Manager", "asd@123")
        result_arr = lr.search(args.enc_query)

    except LdapEncException as e:
        print >> sys.stderr, e
        sys.exit(1)

    if args.file:
        with open(args.file, "w") as enc_file:
            for result in result_arr:
                enc_file.write(result+"\n")
    else:
        for result in result_arr:
            print result


if __name__ == '__main__':
    main()
