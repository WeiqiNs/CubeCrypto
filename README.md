### Rubik's Cube Encryption
[![CI](https://github.com/WeiqiNs/CubeCrypto/actions/workflows/ci.yml/badge.svg)](https://github.com/WeiqiNs/CubeCrypto/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/WeiqiNs/CubeCrypto/branch/master/graph/badge.svg?token=nLPYss2X9g)](https://codecov.io/gh/WeiqiNs/CubeCrypto)
![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-blueviolet)
![Code Style: Flake8](https://img.shields.io/badge/Code%20Style-Flake8-blue)

This repository is the implementation of the Rubik's Cube symmetric encryption protocol described [here](https://github.com/WeiqiNs/HonorThesis).

While running the encryption protocol, we first need to decide an arbitrary length of the Rubik's Cube as well as a key length. The encryption protocol creates a Rubik's Cube object and calls a random generator to generate a key with the desired length. Then we run the encryption protocol with the input of a plaintext message in English with arbitrary length and the randomly generated key. Finally, the encryption protocol outputs the encrypted message in binary. The decryption protocol takes in the binary value and a key and returns the decrypted plaintext in English.

Along with the encryption protocol, we provide some scripts to help users to determine the proper key length for different sizes of Rubik's Cubes and tools to analyze how well the encryption protocol is doing.

In `examples.ipynb` you can find detailed usage of the encryption and decryption protocol.
