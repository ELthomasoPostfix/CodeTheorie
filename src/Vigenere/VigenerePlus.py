"""
This file decrypts a message encrypted using first the vigenere technique and then
a single column transposition.

ct = kolom transpositie
v = vigenere
m = message
(  ct(v(m))  )⁻¹  =  (ct ° v)⁻¹(m) = (v⁻¹ ° ct⁻¹)(m) = v⁻¹(ct⁻¹(m))
"""
