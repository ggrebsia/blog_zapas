from collections import OrderedDict
from tkinter import messagebox

adfgvx_table = [
    ['p', 'h', '0', 'q', 'g', '6'],
    ['4', 'm', 'e', 'a', '1', 'y'],
    ['l', '2', 'n', 'o', 'f', 'd'],
    ['x', 'k', 'r', '3', 'c', 'v'],
    ['s', '5', 'z', 'w', '7', 'b'],
    ['j', '9', 'u', 't', 'i', '8'],
    ['P', 'H', ',', 'Q', 'G', '.'],
    [':', 'M', 'E', 'A', '"', 'Y'],
    ['L', ';', 'N', 'O', 'F', 'D'],
    ['X', 'K', 'R', '?', 'C', 'V'],
    ['S', '!', 'Z', 'W', '-', 'B'],
    ['J', '(', 'U', 'T', 'I', ' '], 
]


adfgvx_letters = "ABCDEFGHIJKL"

def adfgvx_encrypt(plaintext, key):
    adfgvx_text = ''
    for char in plaintext:
        found = False
        for i in range(len(adfgvx_table)): 
            for j in range(len(adfgvx_table[i])): 
                if adfgvx_table[i][j] == char:
                    adfgvx_text += adfgvx_letters[i] + adfgvx_letters[j]
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f"Символ '{char}' отсутствует в таблице ADFGVX.")

    key_len = len(key)
    matrix = [adfgvx_text[i:i + key_len] for i in range(0, len(adfgvx_text), key_len)]
    if len(matrix[-1]) < key_len:
        matrix[-1] = matrix[-1]
    
    sort_key_indx = sorted(range(len(key)), key=lambda x: key[x])
    ciphertext = ""
    for indx in sort_key_indx:
        for row in matrix:
            if indx < len(row):
                ciphertext += row[indx]

    return ciphertext

def adfgvx_decrypt(ciphertext, key):
    key_len = len(key)
    total = len(ciphertext)
    rows = total // key_len
    excees = total % key_len

    key_indx = list(range(len(key)))
    sort_key_indx = sorted(key_indx, key=lambda x: key[x])

    col_lengths = [rows + (1 if i < excees else 0) for i in range(key_len)]
    ciphertext_col = {}
    indx = 0
    for sort_indx in sort_key_indx:
        ciphertext_col[sort_indx] = ciphertext[indx:indx + col_lengths[sort_indx]]
        indx += col_lengths[sort_indx]

    orig_col = [ciphertext_col[i] for i in key_indx]
    adfgvx_text = ""
    for i in range(rows + 1):
        for col in orig_col:
            if i < len(col):
                adfgvx_text += col[i]

    plaintext = ""
    for i in range(0, len(adfgvx_text), 2):
        row = adfgvx_letters.index(adfgvx_text[i])
        col = adfgvx_letters.index(adfgvx_text[i + 1])
        plaintext += adfgvx_table[row][col]

    return plaintext