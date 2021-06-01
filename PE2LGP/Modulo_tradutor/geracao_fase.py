#"Fase de geração"

import csv
from builtins import any as b_any
from ExtensoToInteiro import ExtensoToInteiro

def ordena_dets_num_adverq(traducao):
	"""
	Ordena determinantes, numerais e adverbios de quantidade consoante a LGP.
	:param traducao: frase
	:return:
	"""

	indice = 0

	while indice < len(traducao):

		valor = traducao[indice]
		classe = valor[2]

		if (classe.startswith("DP") or classe.startswith("Z") or classe.startswith("RGQ")) :
			if indice!=len(traducao)-1 and traducao[indice+1][2].startswith("N"):
				temp = valor
				traducao[indice] = traducao[indice + 1]
				traducao[indice + 1] = temp
				indice+=1

		indice+=1


def orden_neg_int(i, counter, exprFaciais, negativa_irregular):
	"""
	Ordena elementos de negação e de interrogação e adiciona as expressões faciais.
	:param i.traducao: frase
	:return:
	"""
	count = 0
	indice = 0


	while indice < len(i.traducao):
		valor = i.traducao[indice]
		classe = valor[2]
		if indice < len(i.traducao) - count:
			if classe.startswith("RN"): # adds "Não" at the end
				# valor = ("{"+valor[0] +"}(negativa)", "{"+valor[0] +"}(negativa)", valor[2])
				# indice_verbo = i.indices_verbo[0]-1
				# if i.traducao[indice_verbo][1] not in negativa_irregular:
				i.traducao.append(valor)
				del i.traducao[indice]
				count += 1
				indice = 0
			if (classe.startswith("PT") or classe.startswith("RGI")) and "INT" in i.tipo[0]:
				# valor = ("{"+valor[0] +"}(interrogativa)", "{"+valor[0] +"}(interrogativa)", valor[2])
				print("valor")
				print(valor)
				i.traducao.append(valor)
				del i.traducao[indice]
				count += 1
		indice += 1


def tempo_verbal(i):
	"""
	Ordena os advérbios de tempo se existirem na frase. Caso contrário adiciona gestos que marcam os tempos verbais.
	:param traducao: frase
	:return:
	"""
	pronomes = {"1S": "eu", "2S": "tu", "3S": "ele", "1P": "nós", "2P": "vós", "3P": "eles"}
	indice_tempo = list(filter(lambda x: x[1][2] == "RGTP" or x[1][2] == "RGTF", enumerate(i.traducao)))

	if indice_tempo:
		temp = i.traducao[indice_tempo[0][0]]
		del i.traducao[indice_tempo[0][0]]
		i.traducao.insert(0, temp)
	
	# Adiciona o pronome pessoal se este ou o sujeito não exisitir e se o pronome não foi o da primeira pessoa no singular
	for indice, valor in enumerate(i.traducao):
		classe = valor[2]
		if classe.startswith("V"):
			# if indice==0 or indice > 0 and not (i.traducao[indice-1][2].startswith("PP") or i.traducao[indice-1][2].startswith("NC")): # or traducao[indice-1][2].startswith("NC")
			if not i.classes_suj:
				pronome = classe[4] + classe[5]
				if pronome in pronomes:
					temp = (pronomes[pronome], pronomes[pronome], "PP")
					i.traducao.insert(indice, temp)
					break

	# else:
	# 	for indice, valor in enumerate(traducao):
	# 		classe = valor[2]
	# 		if classe.startswith("V"):
	# 			if classe[3] == "S" or classe[3] == "I" or classe[3] == "M":
	# 				temp = ("PASSADO", "PASSADO", "RGTP")
	# 				traducao.insert(0, temp)
	# 				break
	# 			if classe[3] == "F":
	# 				traducao.insert(0, ("FUTURO", "FUTURO", "RGTF"))
	# 				break
	# 			if classe[3] == "P":
	# 				break

def nomes_proprios(traducao, palavras_compostas):
	"""
	Identifica nomes próprios usando a notação DT().
	:param traducao: frase
	:param palavras_compostas: palavras compostas
	:return:
	"""

	nomes_proprios_lista = list(filter(lambda x: x[1][2].startswith("NP"), enumerate(traducao)))


	if nomes_proprios_lista:
		indices_nomes = list(list(zip(*nomes_proprios_lista))[0])
		for n in indices_nomes:
			valor = traducao[n][0]
			nome = ""
			if valor in palavras_compostas.values():
				glosa_nome_proprio = ""
				for palavras, v in palavras_compostas.items():
					for p in palavras.split("_"):
						nome = ""
						for l in p:
							nome += l.upper() + "-"
						glosa_nome_proprio += "DT(" + nome[:-1] + ")" + " "
					glosa_nome_proprio = glosa_nome_proprio[:-1]

			else:

				for l in valor:
					letra = l.upper()
					nome += letra + "-"

				glosa_nome_proprio = "DT(" + nome[:-1] + ")"

			traducao[n] = (glosa_nome_proprio, glosa_nome_proprio, traducao[n][2])




def abre_feminino_excepcoes():
	"""
	Trata das palavras no feminino que são excepções à regra.
	:return:
	"""
	excepcoes = {}
	with open('Feminino_excepcoes.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			excepcoes[row[0]] = row[1]


	return excepcoes


def feminino(traducao, excepcoes):
	"""
	Trata da marcação do feminino. Trata também do diminutivo e aumentativo.
	:param traducao: frase
	:param excepcoes: dicionário com as palavras que são excepções e as suas traduções.
	:return:
	"""
	indice = 0
	while indice < len(traducao):
		valor = traducao[indice]
		palavra = valor[0]
		classe = valor[2]
		lema = valor[1]

		if classe.startswith("NC"):

			if palavra not in excepcoes:
				if palavra.lower()!=lema.lower():
					if classe.endswith("D"):
						if classe.startswith("NCFP") and palavra[:-5].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, lema, "A"))
							traducao[indice + 1] = (lema, lema, classe)
							traducao.insert(indice + 2, ("PEQUENO", "PEQUENO", classe))
							indice += 2

						elif classe.startswith("NCFS") and palavra[:-4].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice,(glosa, lema, "A"))
							traducao[indice + 1] = (lema, lema, classe)
							traducao.insert(indice + 2, ("PEQUENO", "PEQUENO", classe))
							indice += 2

						elif classe.startswith("NCFS") and palavra[:-4].lower() == lema[:-1].lower():
							traducao[indice] = (lema, lema, classe)
							traducao.insert(indice + 1, ("PEQUENO", "PEQUENO", classe))
							indice += 1

						elif classe.startswith("NCFP") and palavra[:-5].lower() == lema[:-1].lower():
							traducao[indice] = (lema, lema, classe)
							traducao.insert(indice + 1, ("PEQUENO", "PEQUENO", classe))
							indice += 1

						else:
							if classe.endswith("D"):
								diminutivo = "PEQUENO"
								traducao.insert(indice + 1, (diminutivo, diminutivo, classe))
								traducao[indice] = (
								traducao[indice][1], traducao[indice][1], traducao[indice][2])
								indice += 1

							elif classe.endswith("A"):
								traducao.insert(indice + 1, ("GRANDE", "GRANDE", classe))
								traducao[indice] = (traducao[indice][1], traducao[indice][1], traducao[indice][2])
								indice += 1




					elif classe.endswith("A"):
						if classe.startswith("NCFP") and palavra[:-5].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, lema, "A"))
							traducao[indice + 1] = (lema, lema, classe)
							traducao.insert(indice + 2, ("GRANDE", "GRANDE", classe))
							indice += 2

						elif classe.startswith("NCFS") and palavra[:-4].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, lema, "A"))
							traducao[indice + 1] = (lema, lema, classe)
							traducao.insert(indice + 2, ("GRANDE", "GRANDE", classe))
							indice += 2

						elif classe.startswith("NCFS") and palavra[:-4].lower() == lema[:-1].lower():
							traducao[indice] = (lema, lema, classe)
							traducao.insert(indice + 1, ("GRANDE", "GRANDE", classe))
							indice += 1

						elif classe.startswith("NCFP") and palavra[:-5].lower() == lema[:-1].lower():
							traducao[indice] = (lema, lema, classe)
							traducao.insert(indice + 1, ("GRANDE", "GRANDE", classe))
							indice += 1


					else:
						if classe.startswith("NCFP") and palavra[:-1].lower() != lema.lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, lema, "A"))
							traducao[indice + 1] = (lema, lema, classe)
							indice += 1
						elif classe.startswith("NCFS") and palavra.lower() != lema.lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, lema, "A"))
							traducao[indice + 1] = (lema, lema, classe)
							indice += 1

			else:
				if palavra.lower() != lema.lower():
					if classe.endswith("D"):
						diminutivo = "PEQUENO"
						if "mulher" in excepcoes[palavra].split():
							traducao.insert(indice, ("mulher", lema, "A"))
							traducao[indice + 1] = (excepcoes[palavra].split()[1], lema, classe)
							traducao.insert(indice + 2, ("PEQUENO", "PEQUENO", classe))
							indice += 2

						else:
							traducao[indice] = (excepcoes[palavra], lema, classe)
							traducao.insert(indice + 1, ("PEQUENO", "PEQUENO", classe))
							indice += 1

					elif classe.endswith("A"):
						if "mulher" in excepcoes[palavra].split():

							traducao.insert(indice, ("mulher", lema, "A"))
							traducao[indice + 1] = (excepcoes[palavra].split()[1], lema, classe)
							traducao.insert(indice + 2, ("GRANDE", "GRANDE", classe))
							indice += 2

						else:
							traducao[indice] = (excepcoes[palavra], lema, classe)
							traducao.insert(indice + 1, ("GRANDE", "GRANDE", classe))
							indice += 1
					else:

						traducao[indice] = (excepcoes[palavra], lema, classe)


		indice += 1


def remove_prep(traducao):
	indice = 0
	while indice < len(traducao):
		valor = traducao[indice]
		classe = valor[2]

		if classe.startswith("SP"):
			del traducao[indice]
			indice -= 1
		indice +=1

def remove_ser_estar(traducao):
	indice = 0
	count = 0
	while indice < len(traducao)-count:
		classe = traducao[indice][2]
		lema = traducao[indice][1]
		palavra = traducao[indice][0]
		
		if lema.lower() =="ser" or lema.lower() == "estar":
			del traducao[indice]
			count +=1
		elif classe == "CC" and palavra.lower() == "e":
			del traducao[indice]
			count += 1
		indice+=1



def cliticos(traducao):
	"""
	Trata dos pronomes clíticos.
	:param traducao: frase
	:return:
	"""
	for indice, valor in enumerate(traducao):
		classe = valor[2]
		palavra = valor[0]
		if classe.startswith("PP"):

			if palavra.lower() == "te" or palavra.lower() == "ti":
				traducao[indice] = ("TU", "TU", classe)

			elif palavra.lower() == "me" or palavra.lower() == "mim":
				traducao[indice] = ("EU", "EU", classe)

			elif palavra.lower() == "nos":
				traducao[indice] = ("NÓS", "NÓS", classe)

			elif palavra.lower() == "se":
				traducao[indice] = ("", "", classe)

def converte_glosas(i, counter, exprFaciais, negativa_irregular):
	"""
	Converte as palavras em glosas.
	:param traducao: frase
	:return:
	"""
	verbo_neg_irregular = False
	indice = 0
	while indice < len(i.traducao):
		valor = i.traducao[indice]
	# for indice, valor in enumerate(i.traducao):
		classe = valor[2]
		lema = valor[1]
		palavra = valor[0]

		print(palavra)

		if not classe.startswith("A") and not classe.startswith("NC"):
			i.traducao[indice] = lema.upper()

		else:
			i.traducao[indice] = palavra.upper()
		# converte _ para - ex. fim_de_semana para fim-de-semana
		if "_" in i.traducao[indice] or "-" in i.traducao[indice]:
			i.traducao[indice] = i.traducao[indice].replace("_", " ").replace("-", " ")

		if "DE" in i.traducao[indice].upper():
			i.traducao[indice] = i.traducao[indice].replace(" DE", "")
		
		if classe.startswith("Z"):
			try:
				int(palavra)
			except ValueError:
				# Transforma numeros por exenso sem ser por extenso
				i.traducao[indice] = str(ExtensoToInteiro(palavra))

		# Adiciona a expressao negativa no verbo
		if classe.startswith("VMI") and "NEG" in i.tipo[0] and lema in negativa_irregular:
			key = str(indice+counter) + "-" + str(indice+counter+1)
			if key in exprFaciais:
				exprFaciais[key].append("negativa_headshake")
			else:
				exprFaciais[key] = ["negativa_headshake"]
			i.traducao[indice] = "NÃO_" + lema.upper()
			verbo_neg_irregular = True
			i.traducao_palavras.append("NÃO")

		# Remove a glosa NAO se for uma negativa irregular
		if verbo_neg_irregular and classe.startswith("RN"):
			del i.traducao[indice]
			indice -= 1
		
		# if verbo_neg_irregular:
		# 	counter -= 1

		if "INT" in i.tipo[0]:
			key = str(indice+counter) + "-" + str(indice+counter+1)
			#Adiciona a expressao da interrogativa parcial no adverbio
			if (classe.startswith("PT") or classe.startswith("RGI")):
				if key in exprFaciais:
					exprFaciais[key].append("interrogativa_parcial")
				else:
					exprFaciais[key] = ["interrogativa_parcial"]
			#Adiciona a expressao da interrogativa total no ultimo gesto da frase
			elif indice==(len(i.traducao)-1):
				if key in exprFaciais:
					exprFaciais[key].append("interrogativa_total")
				else:
					exprFaciais[key] = ["interrogativa_total"]
		
		if not (verbo_neg_irregular and classe.startswith("RN")):
			i.traducao_palavras.append(palavra.upper().replace("_", " ").replace("-", " ").replace(" DE", ""))
		
		indice += 1


		# Adiciona a expressao negativa no gesto manual NÃO
		# if classe.startswith("RN") and "NEG" in i.tipo[0]:
		# 	exprFaciais[str(indice+counter) + "-" + str(indice+counter+1)] = "negativa"

	if "" in i.traducao:
		i.traducao.remove('')

def expressao_olhos_franzidos(tipo, traducao, indice, exprFaciais):
	"""
	Adiciona as expressões faciais em interrogativas globais.
	:param frase: frase
	:param traducao_glosas: frase com algumas regras manuais aplicadas
	:param tags: classes gramaticais das palavras
	:return:
	"""
	if "INT" in tipo[0] or "NEG" in tipo[0]:
		exprFaciais[str(indice) + "-" + str(indice+len(traducao))] = ["olhos_franzidos"]
		# traducao_glosas = "{" + traducao_glosas + "}(q)"

	# return traducao_glosas

def geracao(i, counter, exprFaciais, negativa_irregular):
	"""
	Função principal que aplica as regras manuais anteriores conforme a gramática da LGP.
	:param i: Frase em português (objeto).
	:return: Frase em LGP
	"""

	classes = list(list(zip(*i.traducao))[2])

	# remover preposições
	remove_prep(i.traducao)

	#altera ordem determinantes, numerais e adverbios quantidade
	ordena_dets_num_adverq(i.traducao)

	#nomes próprios
	# nomes_proprios(i.traducao, i.palavras_compostas)

	#feminino
	excepcoes = abre_feminino_excepcoes()
	feminino(i.traducao, excepcoes)

	# remover ser e estar
	remove_ser_estar(i.traducao)

	# transformar cliticos
	cliticos(i.traducao)

	#advérbio de negação e interrogativas parciais (pronomes e advérbios) para o fim da frase
	orden_neg_int(i, counter, exprFaciais, negativa_irregular)

	print(i.traducao)

	#Verbos
	tempo_verbal(i)

	print(i.traducao)

	# passar para glosas && adicionar expressão facial negativa e interrogativa
	converte_glosas(i, counter, exprFaciais, negativa_irregular)

	print(i.traducao)

	# join das glosas da traducao
	# traducao_glosas = " ".join(i.traducao)

	# print(i.traducao)

	# traducao_glosas = traducao_glosas.split(" ")

	# adicionar a expressao "olhos franzidos" à frase toda se for uma interrogativa e/ou negativa
	expressao_olhos_franzidos(i.tipo, i.traducao, counter, exprFaciais)

	return i.traducao, exprFaciais, " ".join(i.traducao_palavras)
