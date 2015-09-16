# Google Analytics Extractor

Follow the tutorial [here](https://developers.google.com/analytics/solutions/articles/hello-analytics-api). I've made it into a module.

## Installing the Google Python API

Instructions are here:

https://developers.google.com/api-client-library/python/start/installation

You need to supply your own `client_secrets.json` file, which you can download from [this link](https://code.google.com/apis/console/). Go to the ``API Access`` link. Make sure that you select an *Installed Application*, not a webapp.

## Using the Google Analytics Extractor

Save the `gaextractor.py` file. This library makes it easier to connect to the Google Analytics API. You use it from within Python scripts.

Example usage:

```python
import gaextractor

authentication = gaextractor.Authentication()
extractor      = gaextractor.Extractor(authentication)
```

If you haven't authenticated before, your web browser will pop up You've now got a properly set up extractor object. Hooray!

By default the extractor object goes to the first account the user can access, the first web property in that account and then the first profile in that web property. If you want to connect to a different property, you can pass the Extractor additional parameters `accountid`, `webpropertyid` and `profileid`. 

You don't need to specify all of them. If you just specify the `profileid` for example, it defaults to the first account and web property, then the specified profile id.

### Listing all the profile IDs

It is tricky to find the profile ID you want. It can be extracted from the URL, but it is easier to use this function.

First initialise your extractor object. Then run the following:

```python
extractor.listprofiles()
```

This prints out a comma separated list of Profile Name and Profile ID.


### Running a query

With the extractor object, you can run queries with it.

```python
extractor.extractdata(['ga:visits'])
```

This query is the simplest query you can run, it just asks the API for one metric. It defaults to data from today.

#### Additional metrics

The one argument passed to the extractdata function above was the metrics. I only asked for one metric, but you can give it more if you pass them as a python list.

Here is more information on the metrics.

https://developers.google.com/analytics/devguides/reporting/core/v3/reference#metrics

#### Dimensions

Metrics by themselves aren't very interesting. To cut the data in different ways, pass the `dimensions` parameter to the function.

```python
extractor.extractdata(['ga:visits'],
                      dimensions = ['ga:browser', 'ga:city'])
```

More information about dimensions here:

https://developers.google.com/analytics/devguides/reporting/core/v3/reference#dimensions

If you only want 1 dimension, you still need to pass it as a list.

#### Start and end dates

If you don't specify a start or an end date, it defaults to today's date for both. To extract a different range of data, specify the ``start_date`` and ``end_date`` parameters, passing them dates in the format '2013-04-09' for 9th April 2013.

#### Start index

The API only returns 10k rows. Pass the ``start_index`` parameter to start at a different point, just like excellent analytics.

#### Filters

Similar to the Metrics and Dimensions, pass a list that defines the filters you want to apply.

Information on the filter syntax can be found here:

https://developers.google.com/analytics/devguides/reporting/core/v3/reference#filters

### Extracting the data

Once you're run ``extractdata``, there are two methods for outputting data - ``to_csv`` and ``to_json``.

Running these by themselves creates a `outfile.csv` file, or a `outfile.json` file. Specify either the `outfile` or the `pretty` attribute to modify the default behaviour.

    def to_csv(self, filename = "outfile.csv"):
        """
        Write the GA data to a CSV file with the correct header.
        Requires that you have run extractdata first.
        """



    def to_json(self, filename = "outfile.json", pretty = True):
        """
        Write the GA data to a JSON file.
        Requires that you have run extractdata first.

        `pretty` says if we write it out with an indent or not
        """
