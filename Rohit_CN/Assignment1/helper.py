#!/usr/bin/env python3
from sympy import Poly

CRCPolynomials = {
    "CRC-8"       : "x^8 + x^7 + x^6 + x^4 + X^2 +1",
    "CRC-10"      : "x^10 + x^9 + x^5 + x^4 + x^1 + 1",
    "CRC-16"      : "x^16 + x^15 + x^2 + 1",
	"CRC-32"      : "x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + 1"  
}

def convToBinary(key):
	polynomial = Poly(CRCPolynomials[key])
	print(polynomial)
	binary = bin(polynomial.eval(2))
	return binary[2:]
	
	