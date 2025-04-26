### Rubik's Cube Encryption
[![codecov](https://codecov.io/gh/WeiqiNs/CubeCrypto/graph/badge.svg?token=nLPYss2X9g)](https://codecov.io/gh/WeiqiNs/CubeCrypto)
[![Documentation Status](https://readthedocs.org/projects/pydocs/badge/?version=latest)](https://pydocs.readthedocs.io/en/latest/?badge=latest)

This repository is the implementation of the Rubik's Cube symmetric encryption protocol described [here](https://github.com/Weiqi97/Honor-Thesis).

While running the encryption protocol, we first need to decide an arbitrary length of the Rubik's Cube as well as a key length. The encryption protocol creates a Rubik's Cube object and calls a random generator to generate a key with the desired length. Then we run the encryption protocol with the input of a plaintext message in English with arbitrary length and the randomly generated key. Finally, the encryption protocol outputs the encrypted message in binary. The decryption protocol takes in the binary value and a key and returns the decrypted plaintext in English.

Along with the encryption protocol, we provide some scripts to help users to determine the proper key length for different sizes of Rubik's Cubes and tools to analyze how well the encryption protocol is doing.

In `examples.ipynb` you can find detailed usage of the encryption and decryption protocol.
