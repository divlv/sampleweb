# import os
import json
import urllib.request
import ssl
import pickledb
import logging

class DataLoader:

    cacheEnabled = False
    # Auth Token for REST services. To be implemented...
    authToken = "ecd2ead6-0ca3-43e2-a59e-3efa28b3c6d1" # Default Latvian token
    country = "c-1" # Latvia

    #RESTserver = "http://localhost:8080"
    RESTserver = "https://ciprest.memoriali.org"

    totalsRestEndpoint = "%s/v1/%s/country/%s/totals" % (RESTserver, authToken, country)
    regionsRestEndpoint = "%s/v1/%s/country/%s/regions" % (RESTserver, authToken, country)
    districtsRestEndpoint = "%s/v1/%s/country/%s/regions/%s/districts" % (RESTserver, authToken, country, "%s")
    memorialsByDistrictRestEndpoint = "%s/v1/%s/country/%s/districts/%s/memorials" % (RESTserver, authToken, country, "%s")
    memorialByIdRestEndpoint = "%s/v1/%s/country/%s/memorial/%s/pagesize/20/page/%s" % (RESTserver, authToken, country, "%s", "%s")
    memorialsGeoData = "%s/v1/%s/country/%s/memorials/gson" % (RESTserver, authToken, country)



    def __init__(self):
       pathToCacheFile="c:/tmp/cache.pdb"
       self.pdb_cache = pickledb.load(pathToCacheFile, False)
       self.sslcontext = ssl._create_unverified_context()
       logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
       #... filename='example.log' ...


    def loadTotals(self):
        if self.cacheEnabled:
            jsonData = self.pdb_cache.get("totals")
        else:
            jsonData = False
        #jsonData = False
        if jsonData==False:
            logging.debug("No cache data found for totals. Loading from remote %s", self.totalsRestEndpoint)
            with urllib.request.urlopen(self.totalsRestEndpoint, context=self.sslcontext) as url:
                totalNumbers = json.loads(url.read().decode())
            if self.cacheEnabled:
                self.pdb_cache.set("totals", totalNumbers)
                self.pdb_cache.dump()
                logging.debug("Totals data loaded and saved to cache")
        else:
            logging.debug("Getting totals data from cache.")
            totalNumbers = jsonData
        return totalNumbers


    def loadRegions(self):
        if self.cacheEnabled:
            jsonData = self.pdb_cache.get("regions")
        else:
            jsonData = False
        #jsonData = False
        if jsonData==False:
            logging.debug("No cached data found for regions. Loading from remote %s", self.regionsRestEndpoint)
            with urllib.request.urlopen(self.regionsRestEndpoint, context=self.sslcontext) as url:
                regionsFromRest = json.loads(url.read().decode())
            if self.cacheEnabled:
                self.pdb_cache.set("regions", regionsFromRest)
                self.pdb_cache.dump()
                logging.debug("Regions data loaded and saved to cache")
        else:
            logging.debug("Getting regions data from cache.")
            regionsFromRest = jsonData
        return regionsFromRest

    def loadDistricts(self, regionid):
        jsonKey = "districts" + str(regionid)
        if self.cacheEnabled:
            jsonData = self.pdb_cache.get(jsonKey)
        else:
            jsonData = False
        restEndPoint = self.districtsRestEndpoint % regionid
        #jsonData = False
        if jsonData==False:
            logging.debug("No cached data found for districts. Loading from remote %s", restEndPoint)
            with urllib.request.urlopen(restEndPoint, context=self.sslcontext) as url:
                districtsFromRest = json.loads(url.read().decode())
            if self.cacheEnabled:
                self.pdb_cache.set(jsonKey, districtsFromRest)
                self.pdb_cache.dump()
                logging.debug("Districts data loaded and saved to cache")
        else:
            logging.debug("Getting districts data from cache.")
            districtsFromRest = jsonData
        return districtsFromRest

    def loadMemorials(self, districtid):
        jsonKey = "memorials" + str(districtid)
        if self.cacheEnabled:
            jsonData = self.pdb_cache.get(jsonKey)
        else:
            jsonData = False
        restEndPoint = self.memorialsByDistrictRestEndpoint % districtid
        #jsonData = False
        if jsonData==False:
            logging.debug("No cached data found for memorials by district. Loading from remote %s", restEndPoint)
            with urllib.request.urlopen(restEndPoint, context=self.sslcontext) as url:
                districtsFromRest = json.loads(url.read().decode())
            if self.cacheEnabled:
                self.pdb_cache.set(jsonKey, districtsFromRest)
                self.pdb_cache.dump()
                logging.debug("Memorials by district data loaded and saved to cache")
        else:
            logging.debug("Getting memorials by district from cache.")
            districtsFromRest = jsonData
        return districtsFromRest

    def loadMemorialById(self, memorialid, pageno, pagesize):
        jsonKey = "memorial" + str(memorialid)+"pn"+str(pageno)+"ps"+str(pagesize)
        if self.cacheEnabled:
            jsonData = self.pdb_cache.get(jsonKey)
        else:
            jsonData = False
        restEndPoint = self.memorialByIdRestEndpoint % (memorialid, pageno)
        logging.debug("Loading soldiers from :"+restEndPoint)

        #jsonData = False
        if jsonData==False:
            logging.debug("No cached data found for memorials by id. Loading from remote %s", restEndPoint)
            with urllib.request.urlopen(restEndPoint, context=self.sslcontext) as url:
                memorialFromRest = json.loads(url.read().decode())
            if self.cacheEnabled:
                self.pdb_cache.set(jsonKey, memorialFromRest)
                self.pdb_cache.dump()
                logging.debug("Memorial by id information loaded and saved to cache")
        else:
            logging.debug("Getting memorial information by id from cache.")
            memorialFromRest = jsonData
        return memorialFromRest
