#!/usr/bin/python
# -*- coding: utf-8 -*-


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
import datetime
import httplib2
import json
import csv
import json

    
# Declare constants and set configuration values
# The file with the OAuth 2.0 Client details for authentication and 
# authorization.
CLIENT_SECRETS = 'client_secrets.json'
# A helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS
# The Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly', #, 'http://www.googleapi.com/analytics/v3alpha/',
    message=MISSING_CLIENT_SECRETS_MESSAGE)
# A file to store the access token
TOKEN_FILE_NAME = 'analytics.dat'

class Authentication:
    def __init__(self):
        self.credentials = self.prepare_credentials()

    def prepare_credentials(self):
      # Retrieve existing credendials
      storage = Storage(TOKEN_FILE_NAME)
      credentials = storage.get()

      # If existing credentials are invalid and Run Auth flow
      # the run method will store any new credentials
      if credentials is None or credentials.invalid:
        #run Auth Flow and store credentials
        credentials = run_flow(FLOW, storage)

      return credentials


    def initialize_service(self):
      # 1. Create an http object
      http = httplib2.Http()

      # 2. Authorize the http object
      # In this tutorial we first try to retrieve stored credentials. If
      # none are found then run the Auth Flow. This is handled by the
      # prepare_credentials() function defined earlier in the tutorial
      http = self.credentials.authorize(http)  # authorize the http object

      # 3. Build the Analytics Service Object with the authorized http 
      # object
      return build('analytics', 'v3', http=http)

class Extractor:
    def __init__(self, authentication, accountid = None, webpropertyid = None,
            profileid = None):

        self.service = authentication.initialize_service()

        self.today = datetime.datetime.today().strftime("%Y-%m-%d")

        # Initialise all the ids.
        if accountid == None:
            self.getfirstaccountid()
        else:
            self.accountid = accountid
        self.checkaccountid()

        if webpropertyid == None:
            self.getfirstwebpropertyid()
        else:
            self.webpropertyid = webpropertyid
        self.checkwebpropertyid()

        if profileid == None:
            self.getfirstprofileid()
        else:
            self.profileid = profileid
        self.checkprofileid()

        # now we have a properly set up extractor object.
        # there are two useful functions:
        #  - listprofiles()
        #       - This lists all the profile IDs. It is otherwise a bit tricky
        #         to get these out.
        #  - extractdata(metrics = [],
        #                dimensions = [],
        #                start_date,
        #                end_date,
        #                start_index (for pagnation),
        #                filters = [])


    def getfirstaccountid(self):
        """
        sets the first account in the profile.
        """
        accounts = self.service.management().accounts().list().execute()
        print accounts
        self.accountid = accounts.get('items')[0].get('id')
        print self.accountid
    def checkaccountid(self):
        """
        Checks that the account id is valid. Do this by checking there are
        webproperties associated with it.
        """
        wps = self.service.management().webproperties().list(accountId =
                self.accountid).execute()

    def getfirstwebpropertyid(self):
        """
        sets the first web property in the account
        """
        wpgetter = self.service.management().webproperties()
        wplist   = wpgetter.list(accountId=self.accountid).execute()
        print wplist
        for item in wplist.get('items'):
            if item['id'] == 'UA-246109-80':
                self.webpropertyid = item['id']#APP Traffic
        print self.webpropertyid
        #self.webpropertyid = wplist.get('items')[0]['id']
    def checkwebpropertyid(self):
        """
        checks that the webproperty is valid.
        """
        self.service.management().profiles().list(accountId = self.accountid,
                webPropertyId = self.webpropertyid).execute()

    def getfirstprofileid(self):
        """
        sets the first profile in the web property
        """
        profilegetter = self.service.management().profiles()
        profilelist   = profilegetter.list(accountId = self.accountid,
                webPropertyId = self.webpropertyid).execute()
        self.profileid = profilelist.get('items')[0]['id']
    def checkprofileid(self):
        """
        checks that the profile is valid. Does this by checking the number of
        visits for today.
        """ 
        self.service.data().ga().get(
                ids = "ga:"+self.profileid,
                start_date = self.today,
                end_date   = self.today,
                metrics    = "ga:visits"
                ).execute()

    def listprofiles(self):
        """
        Prints out a list of all the profiles in the given webproperty.
        """
        profiles = self.service.management().profiles().list(accountId = 
                self.accountid, webPropertyId = self.webpropertyid).execute()

        print "Profile name, Profile ID"
        for profile in profiles['items']:
            print "%s, %s" % (profile['name'], profile['id'])

    def set_all_app_traffic_profile_id(self):
        profiles = self.service.management().profiles().list(accountId=
                                                             self.accountid, webPropertyId=self.webpropertyid).execute()
        for profile in profiles['items']:
            if profile['id'] == 89307485:
                self.profileid = profile['id']
            print "%s, %s" % (profile['name'], profile['id'])
        return self.profileid

    def extractdata(self,
                    metrics, 
                    dimensions  = None,
                    start_date  = None,
                    end_date    = None,
                    start_index = None,
                    filters     = None,
                    max_results = None,
                    segment     = None):
        """
        Extracts the data from the API. There are a lot of options, the only one
        that you have to provide is a list of the 'metrics' - the things you are
        interested in measuring.

        Everything else defaults to ``None``, but if you specify them then it
        makes the query more specific.

        """
        # This function's main purpose is to encode the url properly. Each
        # parameter for the URL is slightly different.

        # First, encode the profile ID
        ids = "ga:%s" % self.profileid
        print ids
        # Encode the metrics
        metrics = ','.join(metrics)
        print metrics
        # Encode the dimensions, if they exist
        if dimensions is not None:
            dimensions = ','.join(dimensions)

        # Encode the start_date, defaults to today if it isn't supplied.
        if start_date is None:
            start_date = self.today

        # Encode the end_date, defaults to today if it isn't supplied.
        if end_date is None:
            end_date = self.today

        # Don't need to encode the start_index

        # Encode the filters
        if filters is not None:
            filters = ','.join(filters)

        self.data = self.service.data().ga().get(ids = ids, 
                                                 metrics = metrics,
                                                 dimensions = dimensions,
                                                 start_date = start_date, 
                                                 end_date = end_date,
                                                 start_index = start_index, 
                                                 filters = filters, 
                                                 max_results = max_results,
                                                 segment = segment).execute()
        return self.data

    def to_csv(self, filename = "outfile.csv"):
        """
        Write the GA data to a CSV file with the correct header.
        Requires that you have run extractdata first.
        """

        outfile = open(filename, "wb")
        columns = [i[u'name'] for i in self.data['columnHeaders']]
        outwriter = csv.DictWriter(outfile, fieldnames=columns)

        outwriter.writeheader()
        for row in self.data['rows']:
            # make the unicode encoding correct for the row before writing
            unicoderow = [i.encode("utf-8") for i in row]
            outwriter.writerow(dict(zip(columns, unicoderow)))

        outfile.close()

    def to_json(self, filename = "outfile.json", pretty = True):
        """
        Write the GA data to a JSON file.
        Requires that you have run extractdata first.

        ``pretty`` says if we write it out with an indent or not
        """

        outfile = open(filename, "wb")
        json.dump(self.data, 
                  outfile, 
                  indent=2)
        outfile.close()
