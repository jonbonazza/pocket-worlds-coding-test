from encoder import ShortURLEncoder
from pymongo import MongoClient
from pymongo.database import Database
from bson.objectid import ObjectId

class DBInfo:
    name : str
    host : str
    port : int
    
    def __init__(self, name : str, host : str, port : int) -> None:
        self.name = name
        self.host = host
        self.port = port

class URLRepository:
    """
    This URLRepository uses MongoDB for storage. Mongo might be a bit
    overkill for a simple key-value store and something like Zookeeper
    or Etcd might have been more appropriate, but in my experience,
    operating both Zookeeper and Etcd at scale are kind of a pain in
    the butt, so I chose Mongo for convenience.
    
    Also, in a production system, I would strap a distributed cache in
    front of this, such as Redis or Hazelcast. This way, you can make
    burst-y access faster and also save on disk IOPS if running on AWS
    or another cloud provider.
    """
    dbinfo : DBInfo
    dbclient : MongoClient
    db : Database
    encoder : ShortURLEncoder
    
    def __init__(self, encoder : ShortURLEncoder, dbinfo : DBInfo) -> None:
        """
        more recent versions of pymongo do not block on creating the client object. 
        The first operation using the client will try to make the connection.
        
        In a production system, we'd probably want to do some basic operation here
        to prime the connection, but I didn't feel it was necessary for this demo, since
        we are running in a controlled environment.
        """ 
        self.dbinfo = dbinfo
        self.dbclient = MongoClient(self.dbinfo.host, self.dbinfo.port)
        self.db = self.dbclient[self.dbinfo.name]
        self.encoder = encoder
    
    def register(self, url: str) -> str:
        """
        Encodes the URL and stores the mapping of encoding -> url in the
        database.
        
        Various mongo exceptions will be thrown in the event of failures.

        Args:
            url (str): the url to encode and store

        Returns:
            str: the encoded url
        """
        encoded : str = self.encoder.encode_short_url(url)
        doc : dict = {
            "encoded": encoded,
            "url": url,
        }
        
        # Ideally we'd create an index on the 'encoded' filed for faster querying.
        self.db.urls.insert_one(doc)
        return encoded
    
    def retrieve(self, encoded : str) -> str:
        """
        Retrieves the raw URL for the provided encoded URL from the database.
        
        Various mongo exceptions will be thrown in the event of failures.

        Args:
            encoded (str): the encoded url

        Returns:
            str: the requested raw url or an empty string if the requested
            url could not be found.
        """
        res = self.db.urls.find_one({"encoded": encoded})
        if res is not None:
            return res["url"]
        
        return ""