import hashlib
import base62

class ShortURLEncoder:
    # I'm not super familiar with fastapi and its concurrency model,
    # but it seems to run with an asynio model. I'm assuming here that
    # I don't need to worry about race conditions as only one instance of
    # the http handler should ever be running in as ingle instance.
    #
    # If I'm incorrect in this assumption, then we'd probably need to
    # wrap this variable in a RWMutex so that we can access it safely.
    counter : int
    
    def __init__(self) -> None:
        self.counter = 0

    def encode_short_url(self, url : str) -> str:
        """
        Encodes a url to a short url. This is done by first MD5 hashing the URL,
        then base62 encoding it before reducing it down to 7 characters. To prevent
        the extremely rare case of a collision, we keep track of a global counter
        that we use as a salt.
        
        Args:
            url (str): the url to be short encoded

        Returns:
            str: the encoded short url
        """
        self.counter+=1
        hashed = hashlib.md5(url.encode()).digest()
        b62 = base62.encodebytes(hashed)
        salt = str(self.counter)
        size = 7 - len(salt)
        return  salt + b62[:size]
