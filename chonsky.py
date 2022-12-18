import copy
import re


def filtrar_regras_maiores(regras, alfabeto, vocabulario):
    copia = copy.deepcopy(regras)
    for chave in copia:
        valores = copia[chave]
        for i in range(len(valores)):
            if len(valores[i]) > 2:
                for j in range(0, len(valores[i]) - 2):
                    if j == 0:
                        regras[chave][i] = regras[chave][i][0] + alfabeto[0]
                    else:
                        regras.setdefault(nova_chave, []).append(valores[i][j] + alfabeto[0])
                    vocabulario.append(alfabeto[0])
                    nova_chave = copy.deepcopy(alfabeto[0])
                    alfabeto.remove(alfabeto[0])
                regras.setdefault(nova_chave, []).append(valores[i][-2:])

    return regras, alfabeto, vocabulario


def filtrar_regras_vazias(regras, vocabulario):
    regras_vazias = []

    copia = copy.deepcopy(regras)
    for chave in copia:
        values = copia[chave]
        for i in range(len(values)):
            if values[i] == 'e' and chave not in regras_vazias:
                regras_vazias.append(chave)
                regras[chave].remove(values[i])
        if len(regras[chave]) == 0:
            if chave not in regras:
                vocabulario.remove(chave)
            regras.pop(chave, None)

    copia = copy.deepcopy(regras)
    for chave in copia:
        values = copia[chave]
        for i in range(len(values)):
            if len(values[i]) == 2:
                if values[i][0] in regras_vazias and chave != values[i][1]:
                    regras.setdefault(chave, []).append(values[i][1])
                if values[i][1] in regras_vazias and chave != values[i][0]:
                    if values[i][0] != values[i][1]:
                        regras.setdefault(chave, []).append(values[i][0])

    return regras, vocabulario


def remover_regras_curtas(regras, vocabulario):
    hash_map = dict(zip(vocabulario, vocabulario))

    for chave in hash_map:
        hash_map[chave] = list(hash_map[chave])

    for letra in vocabulario:
        for chave in regras:
            if chave in hash_map[letra]:
                values = regras[chave]
                for i in range(len(values)):
                    if len(values[i]) == 1 and values[i] not in hash_map[letra]:
                        hash_map.setdefault(letra, []).append(values[i])

    regras, hash_map = primeiro_passo(regras, hash_map)
    return regras, hash_map


def primeiro_passo(regras, hash_map):
    copia = copy.deepcopy(regras)
    for chave in copia:
        valores = copia[chave]
        for i in range(len(valores)):
            if len(valores[i]) == 1:
                regras[chave].remove(valores[i])
        if len(regras[chave]) == 0: regras.pop(chave, None)

    for chave in regras:
        valores = regras[chave]
        for i in range(len(valores)):
            for j in hash_map[valores[i][0]]:
                for k in hash_map[valores[i][1]]:
                    if j + k not in valores:
                        regras.setdefault(chave, []).append(j + k)

    return regras, hash_map


def ultimo_passo(regras, hash_map, estado_inicial):
    for alfabeto in hash_map[estado_inicial]:
        if not regras[estado_inicial] and not regras[let]:
            for v in regras[let]:
                if v not in regras[estado_inicial]:
                    regras.setdefault(estado_inicial, []).append(v)
    return regras


def mostrar_resultado(regras):
    for chave in regras:
        valores = regras[chave]
        for i in range(len(valores)):
            print(chave + '->' + valores[i])
    return 1


import pathlib


def main():
    regras = {}
    vocabulario = []
    alfabeto = list(map(chr, range(97, 123)))

    arquivo = "exemplo.glc"

    with open(arquivo, "r") as file:
        lines = [line.rstrip() for line in file]

    estado_inicial = lines[0][0]
    entrada_regras = []

    for line in lines:
        if "=" in line:
            entrada_regras.append(line.split("="))

    for entrada in entrada_regras:
        for letra in entrada[0]:
            if letra not in vocabulario:
                vocabulario.append(letra)
            if letra in alfabeto:
                alfabeto.remove(letra)
        for letra in entrada[1]:
            if letra not in vocabulario:
                vocabulario.append(letra)
            if letra in alfabeto:
                alfabeto.remove(letra)
        regras.setdefault(entrada[0], []).append(entrada[1])

    regras, alfabeto, vocabulario = filtrar_regras_maiores(regras, alfabeto, vocabulario)
    mostrar_resultado(regras)

    regras, vocabulario = filtrar_regras_vazias(regras, vocabulario)
    mostrar_resultado(regras)

    regras, estado_final = remover_regras_curtas(regras, vocabulario)
    mostrar_resultado(regras)

    regras = ultimo_passo(regras, estado_final, estado_inicial)
    mostrar_resultado(regras)


if __name__ == "__main__":
    main()
