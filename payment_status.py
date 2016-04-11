"""
view file
File: payment_status.py
Description: Cron to update payment status  
Created On: 05-Apr-2016
Created By: binoy@nephoscale.com
"""

#importing the packages
import ConfigParser
from cloudkittyclient import client
from cloudkittyclient.common import utils
import simplejson as json
from bson import json_util
from keystoneclient.v3 import client as keyclient
from payment_service import *
from card_crypt import *
from Crypto.Cipher import AES

#making the keystone client
KEYSTONE_URL = 'http://69.50.235.228:35357/v3/'
KEYSTONE_TOKEN = '92fcb80a8aa24799a2b58cd8502b46dc'
admin_client = keyclient.Client(token=KEYSTONE_TOKEN, endpoint=KEYSTONE_URL)
 
#For importing details from config file
config = ConfigParser.RawConfigParser()
config.read('/etc/cloudkitty/cloudkitty.conf')

# Fetch details from config file for connection part
connection = dict(config.items("keystone_authtoken"))
extra_config = dict(config.items("extra_conf"))

# kwargs for connection
kwargs = {"tenant_name":"admin",
          "auth_url":'http://127.0.0.1:5000/v2.0',
          "username":"admin",
          "password":connection['password'],
          "cloudkitty_version": extra_config['cloudkitty_version'],
        }

# create cipher instance
CIPHER_KEY = "749dd86f607fa53a5890bb8a0f790474"
cipher = AESCipher(CIPHER_KEY)
 
#Calling the cloud kitty client
cloud_kitty = client.get_client(kwargs.get('cloudkitty_version'), **kwargs)
invoice = cloud_kitty.reports.list_invoice(all_tenants='1')
invoice_details_full = json.loads(invoice, object_hook=json_util.object_hook, use_decimal=True)
tenant_list = []

#Iterating through the invoice and setting the dictionary 
for tenant in invoice_details_full:

    try:

        #Getting the tenant data using the tenant id 
        tenants_list = admin_client.projects.get(tenant)
        ccno = cipher.decrypt(getattr(tenants_list, "ccno", None))
        cc_sec_code = cipher.decrypt(getattr(project, "billing_cc_sec_code", None))

        for tenant_data in invoice_details_full[tenant]:
            tenant_details = {}
            tenant_details['payment_status'] = tenant_data['payment_status']
            tenant_details['tenant_name'] = tenant_data['tenant_name']
            tenant_details['ccno'] = ccno
            tenant_details['cc_sec_code'] = cc_sec_code
            tenant_details['balance_cost'] = tenant_data['balance_cost']
            tenant_list.append(tenant_details)
    except Exception, e:
        print e, 'error......................'

#creating the object for payment
payment_client = AuthorizeClient()

#Making each payments
for tenant_data in tenant_list:
    pay_status = payment_client.make_payment(tenant_data['ccno'], "2021-12", tenant_data['balance_cost'])
    print 'pay_status', pay_status['error'], pay_status['resultcode']