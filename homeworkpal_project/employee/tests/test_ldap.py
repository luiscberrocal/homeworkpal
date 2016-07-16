import ldap
from django.test import TestCase
from django_auth_ldap.backend import LDAPBackend

from homeworkpal_project.settings.base import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD
import logging
logger = logging.getLogger(__name__)

class TestLDAP(TestCase):

    def test_get_user(self):
        user = LDAPBackend().populate_user('OAHerrera')
        self.assertIsNotNone(user)
        self.assertEqual('Herrera Valdes', user.last_name)

    def test_search(self):
        try:
            l = ldap.initialize(AUTH_LDAP_SERVER_URI)
            ## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
            ## and do a bind as shown in the above example.
            # you can also set this to ldap.VERSION2 if you're using a v2 directory
            # you should  set the next option to ldap.VERSION2 if you're using a v2 directory
            l.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
            #l.protocol_version = ldap.VERSION3
        except ldap.LDAPError as e:
            print(e)

        ## The next lines will also need to be changed to support your search requirements and directory
        baseDN = "OU=Corp,DC=canal,DC=acp" # "ou=Customers, ou=Sales, o=anydomain.com"
        searchScope = ldap.SCOPE_SUBTREE
        ## retrieve all attributes - again adjust to your needs - see documentation for more options
        retrieveAttributes = ['cn', 'employeeId', 'givenName' 'sn', 'mail', 'company', 'extensionAttribute8', 'telephoneNumber', 'department']
        #searchFilter = "employeeID=179*"
        searchFilter = "cn=cont-vmurillo*"

        try:
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    ## here you don't have to append to a list
                    ## you could do whatever you want with the individual entry
                    ## The appending to list is just for illustration.
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            for r in result_set:
                logger.debug(r)
        except ldap.LDAPError as e:
            print(e)