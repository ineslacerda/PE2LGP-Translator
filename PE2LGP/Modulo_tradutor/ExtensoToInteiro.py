def ExtensoToInteiro(extenso):
    NumDict = {}
    MilharDict = {}

    NumDict["zero"] = 0
    NumDict["um"] = 1
    NumDict["dois"] = 2
    NumDict["três"] = 3
    NumDict["quatro"] = 4
    NumDict["cinco"] = 5
    NumDict["seis"] = 6
    NumDict["sete"] = 7
    NumDict["oito"] = 8
    NumDict["nove"] = 9

    NumDict["dez"] = 10
    NumDict["onze"] = 11
    NumDict["doze"] = 12
    NumDict["treze"] = 13
    NumDict["catorze"] = 14
    NumDict["quinze"] = 15
    NumDict["dezasseis"] = 16
    NumDict["dezassete"] = 17
    NumDict["dezoito"] = 18
    NumDict["dezanove"] = 19

    NumDict["vinte"] = 20
    NumDict["trinta"] = 30
    NumDict["quarenta"] = 40
    NumDict["cinquenta"] = 50
    NumDict["sessenta"] = 60
    NumDict["setenta"] = 70
    NumDict["oitenta"] = 80
    NumDict["noventa"] = 90

    NumDict["cem"] = 100
    NumDict["cento"] = 100 
    NumDict["duzentos"] = 200
    NumDict["trezentos"] = 300
    NumDict["quatrocentos"] = 400
    NumDict["quinhentos"] = 500
    NumDict["seiscentos"] = 600
    NumDict["setecentos"] = 700
    NumDict["oitocentos"] = 800
    NumDict["novecentos"] = 900

    MilharDict["mil"] = 1000
    MilharDict["milhão"] = 1000000
    MilharDict["milhões"] = 1000000
    MilharDict["bilhão"] = 1000000000
    MilharDict["bilhões"] = 1000000000

    resultado = 0
    grupoCorrente = 0

    for word in extenso.split('_'):
        if word in NumDict:
            grupoCorrente += NumDict[word]
        elif word in MilharDict:
            if grupoCorrente == 0: resultado += 1 * MilharDict[word]
            else: resultado  += grupoCorrente * MilharDict[word]
            # resultado += (grupoCorrente == 0 ? 1 : grupoCorrente) * MilharDict[word];
            grupoCorrente = 0

    resultado += grupoCorrente

    return resultado

