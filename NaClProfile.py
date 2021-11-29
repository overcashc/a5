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


class NaClProfile(Profile, NaClDSEncoder):
    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initializes attributes
        """
        super().__init__(dsuserver, username, password)
        self.generate_keypair()

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.
        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str
        """
        self.generate()
        del self.raw_keypair
        #deleting the raw keypair attribute for saving the profile purposes
        return self.keypair

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.
        """
        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair [44:]

    def add_post(self, post: Post) -> None:
        '''
        Encrypts post and adds post to _posts attribute
        '''
        priv_key = self.encode_private_key(self.private_key)
        pub_key = self.encode_public_key(self.public_key)
        box = Box(priv_key, pub_key)
        encoded_post = post.get_entry().encode('utf-8')
        encrypted_entry = box.encrypt(encoded_post, encoder=nacl.encoding.Base64Encoder).decode('utf-8')
        post.set_entry(encrypted_entry)
        super().add_post(post)
    def get_posts(self) -> list:
        '''
        Returns list of decrypted posts
        '''
        encrypted_entries = super().get_posts()
        new_list = []
        priv_key = self.encode_private_key(self.private_key)
        pub_key = self.encode_public_key(self.public_key)
        decrypt_box = Box(priv_key, pub_key)
        for posts in encrypted_entries:
            encoded_entry = posts.get_entry().encode('utf-8')
            plaintext = decrypt_box.decrypt(encoded_entry, encoder=nacl.encoding.Base64Encoder)
            decrypted_entry = plaintext.decode('utf-8')
            new_list.append(Post(decrypted_entry))
        return new_list

    def load_profile(self, path: str) -> None:
        '''
        added support for storing new keypair attributes
        '''
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

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        """
        priv_key = self.encode_private_key(self.private_key)
        pub_key = self.encode_public_key(public_key)
        my_box = Box(priv_key, pub_key)
        message = entry.encode('utf-8')
        encrypted = my_box.encrypt(message, encoder=nacl.encoding.Base64Encoder)
        return encrypted