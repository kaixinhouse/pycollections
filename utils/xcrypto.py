# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA, SHA512
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random


class CryptoAPI(object):

    @staticmethod
    def _pkcs7_padding(data):
        """块对齐"""
        if len(data) % AES.block_size:
            data += '\n' * (AES.block_size - len(data) % AES.block_size)
        return data

    def aes_encrypt(self, data, key):
        """aes 加密"""
        cipher = AES.new(key)
        return cipher.encrypt(self._pkcs7_padding(data))

    def aes_decrypt(self, data, key):
        """aes 解密"""
        cipher = AES.new(key)
        return cipher.decrypt(data)

    def sign(self, signdata, key):
        """进行签名"""
        hash = SHA512.new(signdata)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(hash)
        return signature

    def check_sign(self, data, signature, key):
        """验证签名"""
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(SHA512.new(data), signature):
            print "the signature is authentic"
        else:
            print "the signature is not authentic"

if __name__ == '__main__':
    public_key = RSA.importKey(open('./public_key.pem').read())
    private_key = RSA.importKey(open('./private_key.pem').read())
    message = 'To be Signed\n'
    

    c = CryptoAPI()
    """AES test"""
    aes_key = Random.new().read(32)
    msg = c.aes_encrypt(message, aes_key)
    original_msg = c.aes_decrypt(msg, aes_key)
    print message, '->', 'msg', '->', original_msg, 'end'


    """ RSA test """
    signature = c.sign(message, private_key)
    check = c.check_sign(message, signature, public_key)

