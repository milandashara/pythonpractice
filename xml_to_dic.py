__author__ = 'milanashara'

import urllib2
import xmltodict
import xml.etree.cElementTree as et
import json
import requests

def homepage():
    url='http://si3vwuk1b2b001.pre-prod.skyscanner.local:1252/apiservices/purchases/v1.0/listByProduct?productName=TravelRankings'
    #file = urllib2.urlopen(url)

    response=requests.get(url)
    data=response.json()

    #lines= file.readlines()
    #print lines[0]
    #print data
    count=0
    for product_dto in data["Purchases"]:
        for parameter_dto in product_dto.get("Product",{}).get("Parameters",[]):
            if parameter_dto["ParameterName"] == "TravelRankingsStorageSettings":
                api_key=product_dto["ApiKey"]
                print api_key
                print parameter_dto
                count+=1

    print count
        #print product_dto

    #data = file.read()
    #tree=et.ElementTree(file=file)
    #print et.fromstring(lines[0])
    #root=tree.getroot()

    #file.close()

    #print root

def test_json():

    data="""
    {
        "currency": "GBP",
        "websiteIds": [
            "xpar",
            "xpat",
            "xpau",
            "xpbe",
            "xpbr",
            "xpca",
            "xpde",
            "xpdk",
            "xpes",
            "xpfr",
            "xphk",
            "xpi2",
            "xpid",
            "xpie",
            "xpin",
            "xpit",
            "xpjo",
            "xpjp",
            "xpkr",
            "xpmx",
            "xpmy",
            "xpnl",
            "xpno",
            "xpnz",
            "xpph",
            "xpse",
            "xpsg",
            "xpth",
            "xptw",
            "xpuk",
            "xpus"
        ],
        "routes": [
            [
                "*",
                "*",
                "*"
            ]
        ]
    """

    print json.loads(data)


homepage()
#test_json()