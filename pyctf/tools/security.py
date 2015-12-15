#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import logging
from OpenSSL import crypto, SSL

logger = logging.getLogger("pyctf.security")


def create_self_signed_cert(hostname, cert_file="ssl.crt", key_file="ssl.key",
                            country="US", state="Maine",
                            city="Middle of Nowhere", org="Nonya",
                            unit="Business", force=False):

    if (os.path.exists(cert_file) or os.path.exists(key_file)) and not force:
        raise Exception("Key and/or Cert already exists and force option not set")

    # create a key pair
    k = crypto.PKey()
    logger.debug("Please wait while we generate you a strong SSL key")
    k.generate_key(crypto.TYPE_RSA, 2048)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = country
    cert.get_subject().ST = state
    cert.get_subject().L = city
    cert.get_subject().O = org
    cert.get_subject().OU = unit
    cert.get_subject().CN = hostname

    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(315360000)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
