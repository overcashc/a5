# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin

# Michael Yeung
# myeung2@uci.edu
# 71598323


import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from Profile import Profile, Post
from NaClDSEncoder import NaClDSEncoder
from pathlib import Path
import json, time, os


class NaClProfile(Profile):
    def __init__(self):
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        self.public_key = ''
        self.private_key = ''
        self.keypair = ''
        super().__init__()

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.
        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """
        nacl_enc = NaClDSEncoder()
        nacl_enc.generate()
        self.keypair = nacl_enc.keypair
        self.public_key = nacl_enc.public_key
        self.private_key = nacl_enc.private_key
        return nacl_enc.keypair

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair [44:]

    def add_post(self, post: Post) -> None:
        entry = post['entry']
        encrypted_post = Post(self.encrypt_entry(entry, self.public_key))
        super().add_post(encrypted_post)


    def get_posts(self) -> Post:
        entry_list = super().get_posts()
        new_list = []
        for x in entry_list:
            entry = x['entry']
            nacl = NaClDSEncoder()
            priv_key = nacl.encode_private_key(self.private_key)
            pub_key = nacl.encode_public_key(self.public_key)
            decrypt_box = Box(priv_key, pub_key)
            plaintext = decrypt_box.decrypt(entry)
            decrypted_entry = plaintext.decode('utf-8')
            new_list.append(Post(decrypted_entry))
        return new_list

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.keypair = obj['keypair']
                self.private_key = obj['private_key']
                self.public_key = obj['public_key']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
    """
    TODO: Override the load_profile method to add support for storing a keypair.

    Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
    need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
    load_profile module and add any new attributes you wish to support.

    NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO.
     Just copy the code here and add support for your new attributes.
    """

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        
        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts and this method can call.
        
        :return: bytes 
        """
        nacl = NaClDSEncoder()
        priv_key = nacl.encode_private_key(self.private_key)
        pub_key = nacl.encode_public_key(public_key)
        my_box = Box(priv_key, pub_key)
        message = entry.encode('utf-8')
        encrypted = my_box.encrypt(message)
        return encrypted