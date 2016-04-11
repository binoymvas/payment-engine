"""
This is test file
File : authorizenet.py
Description: API tool 
Created On:  3-Feb-2016
Created By: binoy@nephoscale.com
"""

#importing the packages
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *

class AuthorizeClient:
    
    def __init__(self):
        
        #Authenticating the merchant
        self.merchantAuth = apicontractsv1.merchantAuthenticationType()
        self.merchantAuth.name = '66BPb7jx'
        self.merchantAuth.transactionKey = '3355gugw5HAdBr8x'

    def make_payment(self, ccNumber, ccExpire, amount):

        #CC details
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = ccNumber
        creditCard.expirationDate = ccExpire
        
        #Making the payment type
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard
        
        #Setting the amount and transaction type
        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = Decimal (amount)
        transactionrequest.payment = payment
        
        #creating the transaction request
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = self.merchantAuth
        createtransactionrequest.refId = "MerchantID-0001"
        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()
        
        #Getting the response from the controller
        response = createtransactioncontroller.getresponse()
        
        #Checking the status code.
        if (response.messages.resultCode=="Ok"):
            
            #function to update
            print "avsResultCode=", response.transactionResponse.avsResultCode
            statusCode = {'error': False, 'resultcode': response.messages.resultCode}
        else:
            print "response code: %s" % response.messages.resultCode
            print "error =", response.transactionResponse.errors.error
            statusCode = {'error': True, 'resultcode': response.messages.resultCode}
        return statusCode