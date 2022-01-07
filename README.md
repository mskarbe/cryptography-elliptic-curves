# Cryptography: elliptic curves

Lab work for university course _Introduction to cryptography_.

<!-- TOC -->

- [Cryptography: elliptic curves](#cryptography-elliptic-curves)
  - [Motivation](#motivation)
  - [Lab requirements](#lab-requirements)
  - [Tools used](#tools-used)
  - [Resources](#resources)

<!-- /TOC -->

## Motivation

Elliptic Curve Cryptography (ECC) leverages algebraic structure of elliptic curves over finite fields in order to generate public keys. It can solve the problem of performance-heavy operations with too large keys (f.ex. 2048-bit RSA), as usually for ECC 256 bits are used.

## Lab requirements

- [x] Research two elliptic curves with key lengths 256 and 512 bit. Choose either NIST or brainpool curves.
- [x] Implement an elliptic curve point multiplication configurable for the key lengths 256 and 512 bit.
- [x] Make performance measures for the point multiplication. Be aware that the performance measurements may have some variance, so decide on how many measurements you make and apply basic statics like mean values, variances etc.
- [x] Develop a test strategy (and follow it) in order to make sure, that the algorithm you implemented is a correct ECC pointimplementation. How do you convince me that your implementation is actually not buggy
- [ ] Optionally implement and ECDSA for both key lengths.

## Tools used

The tasks were realized in Python with use of Jupyter Notebook, in order to be able to embed the code easily in the report and to have nicely formatted mathematical formulas. The results are exported to html and pdf formats, but for best readibility (long tables not fitting on pdf f.ex.), please check the notebook via NBViewer [here](https://nbviewer.org/github/mskarbe/cryptography-elliptic-curves/blob/main/ECC-lab.ipynb).

## Resources

Provided in the Jupyter Notebook.
