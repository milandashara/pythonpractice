__author__ = 'milanashara'
import couchbase as cb_lib
from couchbase import Couchbase
from couchbase.bucket import Bucket
def get_connection():
    return Couchbase.connect(
        host='skysgd112.corp.skyscanner.local', bucket='jumala', password='',
        timeout=2.5)

connection=get_connection()
value= {
        "id": "byo00498759482698197861987694387",
        "key": "byo00498759482698197861987694387",
        "value": {
            "display_currency": "GBP",
            "agents": [
                "byza",
                "bysg",
                "byoj",
                "bynz"
            ],
            "markets": [
                {
                    "code": "NZ",
                    "name": "New Zealand"
                },
                {
                    "code": "AU",
                    "name": "Australia"
                },
                {
                    "code": "ZA",
                    "name": "South Africa"
                }
            ],
            "doc_type": "tr_api_info_record"
        }
    }

#connection.add("byo00498759482698197861987694387",value)
print connection.get("byo00498759482698197861987694387").value
connection.set_multi({"test1":"value1","test2":"value2"})
bucket = Bucket('http://skysgd112.corp.skyscanner.local/default',password='')