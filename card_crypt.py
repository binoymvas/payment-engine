#!/usr/bin/env python
"""
This is test file
File : authorizenet.py
Description: API tool 
Created On:  3-Feb-2016
Created By: binoy@nephoscale.com
"""

# keystone auth configuration
import base64
from Crypto import Random
from Crypto.Cipher import AES
from datetime import date

# AESCipher helper class for encryption/decryption
# Rationale: put this class into separate cipher.py file and place it into openstack_dashboard/utils for future importing and usage
class AESCipher:

    _BS = 16

    _pae = lambda self, s: s + (self._BS - len(s) % self._BS) * chr(self._BS - len(s) % self._BS)
    _unpad = lambda self, s : s[0:-ord(s[-1])]

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        """
        Method: encrypt
        Desc: To encrypt the data
        params: enc=> is the value
        Return:Encrypted value
        """
        
        #Encrypting the values
        raw = self._pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        """
        Method: decrypt
        Desc: To decrypt the data
        params: enc=> is the value
        Return: Decrypted value
        """
        
        #Decrypting the values
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self._unpad(cipher.decrypt( enc[16:] ))