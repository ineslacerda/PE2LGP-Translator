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

	print("ordena_dets_num_adverqqqqqqqqqq")

	while indice < len(traducao):

		valor = traducao[indice]
		classe = valor[2]

		print(valor)
		# classe.startswith("Z") 
		if (classe.startswith("DP") or classe.startswith("RGQ")):
			if indice!=len(traducao)-1 and (traducao[indice+1][2].startswith("N") or traducao[indice+1][2].startswith("AQ")):
				temp = valor
				traducao[indice] = traducao[indice + 1]
				traducao[indice + 1] = temp
				indice-=1

		indice+=1


def orden_neg(i, counter, exprFaciais, negativa_irregular):
	"""
	Ordena elementos de negação e de interrogação.
	:param i.traducao: frase
	:return:
	"""
	count = 0
	indice = 0

	int_parcial = False
	while indice < len(i.traducao) - count:
		valor = i.traducao[indice]
		classe = valor[2]
		if classe.startswith("NEGA") or "NEGA" in classe: # adds "Não" at the end
			# valor = ("{"+valor[0] +"}(negativa)", "{"+valor[0] +"}(negativa)", valor[2])
			# indice_verbo = i.indices_verbo[0]-1
			# if i.traducao[indice_verbo][1] not in negativa_irregular:
			i.traducao.append(valor)
			del i.traducao[indice]
			i.traducao.append(('não', 'não', 'RN'))
			count += 1
			indice = -1

		elif classe.startswith("RN"):
			del i.traducao[indice]
			indice = -1
		
		#remove verbo "ficar" se for uma interrogativa parcial --> predicado de estado
		if valor[1].lower() == "ficar" and classe.startswith("V") and int_parcial:
			del i.traducao[indice]
			indice = -1
		indice += 1

def orden_int(i, counter, exprFaciais, negativa_irregular):
	"""
	Ordena elementos de negação e de interrogação.
	:param i.traducao: frase
	:return:
	"""
	count = 0
	indice = 0

	int_parcial = False
	while indice < len(i.traducao) - count:
		valor = i.traducao[indice]
		classe = valor[2]
		
		if (classe.startswith("PT") or classe.startswith("RGI")) and "INT" in i.tipo[0]:
			# valor = ("{"+valor[0] +"}(interrogativa)", "{"+valor[0] +"}(interrogativa)", valor[2])
			i.traducao.append(valor)
			del i.traducao[indice]
			int_parcial = True
			count += 1
			indice = -1
		
		indice += 1

def tempo_verbal(i):
	"""
	Ordena os advérbios de tempo se existirem na frase. Caso contrário adiciona gestos que marcam os tempos verbais.
	:param traducao: frase
	:return:
	"""
	pronomes = {"1S": "eu", "2S": "tu", "3S": "ele", "1P": "nós", "2P": "vós", "3P": "eles"}
	indice_tempo = list(filter(lambda x: x[1][2] == "RGT" or x[1][2] == "RGTP" or x[1][2] == "RGTF", enumerate(i.traducao)))

	# Adiciona tempo verbal no início da frase
	if indice_tempo:
		temp = i.traducao[indice_tempo[0][0]]
		del i.traducao[indice_tempo[0][0]]
		i.traducao.insert(0, temp)
	
	# Adiciona o pronome pessoal se este ou o sujeito não exisitir e se o pronome não foi o da primeira pessoa no singular
	for indice, valor in enumerate(i.traducao):
		classe = valor[2]
		if classe.startswith("V"):
			if i.obj_verb_trans and valor[1].lower() == "chocar":
				index = list(i.obj_verb_trans.keys())[0]
				if i.obj_verb_trans[index] == "obl":
					i.traducao[indice] =  (valor[0], i.traducao[indice][1] + "_com_pessoa", classe)
				elif i.obj_verb_trans[index] == "obj" and index.lower() == "parede":
					i.traducao[indice] =  (valor[0], i.traducao[indice][1] + "_com_parede", classe)
			# if indice==0 or indice > 0 and not (i.traducao[indice-1][2].startswith("PP") or i.traducao[indice-1][2].startswith("NC")): # or traducao[indice-1][2].startswith("NC")
			if not i.classes_suj and (valor[1].lower() != "começar" and valor[1].lower() != "haver"):
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

		print("femininooooo")
		print(palavra)
		print(lema)

		if classe.startswith("NC"):

			if palavra not in excepcoes:
				if palavra.lower()!=lema.lower():
					if classe.endswith("D"):
						if classe.startswith("NCFP") and palavra[:-5].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, glosa, "A"))
							traducao[indice + 1] = (lema, lema, classe + "_COMP")
							traducao.insert(indice + 2, ("PEQUENO", "PEQUENO", classe))
							indice += 2

						elif classe.startswith("NCFS") and palavra[:-4].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice,(glosa, glosa, "A"))
							traducao[indice + 1] = (lema, lema, classe + "_COMP")
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
							traducao.insert(indice, (glosa, glosa, "A"))
							traducao[indice + 1] = (lema, lema, classe + "_COMP")
							traducao.insert(indice + 2, ("GRANDE", "GRANDE", classe))
							indice += 2

						elif classe.startswith("NCFS") and palavra[:-4].lower() != lema[:-1].lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, glosa, "A"))
							traducao[indice + 1] = (lema, lema, classe + "_COMP")
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
							traducao.insert(indice, (glosa, glosa, "A"))
							traducao[indice + 1] = (lema, lema, classe + "_COMP")
							indice += 1
						elif classe.startswith("NCFS") and palavra.lower() != lema.lower():
							glosa = "MULHER"
							traducao.insert(indice, (glosa, glosa, "A"))
							traducao[indice + 1] = (lema, lema, classe + "_COMP")
							indice += 1

			else:
				if palavra.lower() != lema.lower():
					if classe.endswith("D"):
						diminutivo = "PEQUENO"
						if "mulher" in excepcoes[palavra].split():
							traducao.insert(indice, ("MULHER", "MULHER", "A"))
							traducao[indice + 1] = (excepcoes[palavra].split()[1], lema, classe + "_COMP")
							traducao.insert(indice + 2, ("PEQUENO", "PEQUENO", classe))
							indice += 2

						else:
							traducao[indice] = (excepcoes[palavra], lema, classe)
							traducao.insert(indice + 1, ("PEQUENO", "PEQUENO", classe))
							indice += 1

					elif classe.endswith("A"):
						if "mulher" in excepcoes[palavra].split():

							traducao.insert(indice, ("MULHER", "MULHER", "A"))
							traducao[indice + 1] = (excepcoes[palavra].split()[1], lema, classe + "_COMP")
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

		# converte _ para - ex. fim_de_semana para fim de semana
		if "_" in traducao[indice][1] or "-" in traducao[indice][1]:
			traducao[indice] = (valor[0], traducao[indice][1].replace("_", " ").replace("-", " "), classe)

		if "de " in traducao[indice][1] or "para " in traducao[indice][1]:
			traducao[indice] =  (valor[0], traducao[indice][1].replace("de ", "").replace("para ", ""), classe)
		
		if classe.startswith("SP") or classe.startswith("PR"):
			if valor[1] == "de" and traducao[indice+1][2].startswith("PP"):
				traducao[indice+1] =  ("d" + traducao[indice+1][0], "d" + traducao[indice+1][1], traducao[indice+1][2])
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
				del traducao[indice]
				indice -= 1

def expressoes_faciais(i, counter, exprFaciais, negativa_irregular, gestos_compostos):
	"""
	Converte as palavras em glosas.
	:param traducao: frase
	:return:
	"""
	verbo_neg_irregular = False
	adverbio_negacao =  False
	indice = 0
	while indice < len(i.traducao):
		valor = i.traducao[indice]
	# for indice, valor in enumerate(i.traducao):
		classe = valor[2]
		lema = valor[1]
		palavra = valor[0]

		# if not classe.startswith("A") and not classe.startswith("NC"):
		# 	i.traducao[indice] = lema.upper()

		# else:
		# 	i.traducao[indice] = palavra.upper()

		# Adiciona a expressao negativa
		if "NEG" in i.tipo[0]:
			key = str(indice+counter) + "-" + str(indice+counter+1)
				
			# Adiciona a expressao negativa no verbo se for negação irregular
			if classe.startswith("VMI") and "NEGA" in classe and lema in negativa_irregular:
				if key in exprFaciais:
					exprFaciais[key].append("negativa_headshake")
				else:
					exprFaciais[key] = ["negativa_headshake"]

				i.traducao[indice] = (palavra, "NÃO_" + lema.upper(), classe)
				verbo_neg_irregular = True
				i.traducao_palavras.append("NÃO")
			# Adicionar expressão no adverbio de negação
			if classe.startswith("NEGA"):
				if key in exprFaciais:
					exprFaciais[key].append("negativa_headshake")
				else:
					exprFaciais[key] = ["negativa_headshake"]
				i.traducao[indice] = (palavra, lema.replace(" ", "_").upper(), classe)
				adverbio_negacao = True	
		
		print("negaaaa")
		print(verbo_neg_irregular and classe.startswith("RN"))
		print(palavra)

		# Remove a glosa NAO se for uma negativa irregular or um advérbio de negação
		if (verbo_neg_irregular or adverbio_negacao) and classe.startswith("RN"):
			del i.traducao[indice]
			indice -= 1
		
		# Adicionar expressão da interrogativa
		if "INT" in i.tipo[0]:
			key = str(indice+counter) + "-" + str(indice+counter+1)
			#Adiciona a expressao da interrogativa parcial no adverbio
			if (classe.startswith("PT") or classe.startswith("RGI")):
				if key in exprFaciais:
					exprFaciais[key].append("interrogativa_parcial")
				else:
					exprFaciais[key] = ["interrogativa_parcial"]
			#Adiciona a expressao da interrogativa total na preposição e no ultimo gesto da frase
			elif classe.startswith("Fc") or classe.startswith("CC") or classe.startswith("CS") or indice==(len(i.traducao)-1):
				if key in exprFaciais:
					exprFaciais[key].append("interrogativa_total")
				else:
					exprFaciais[key] = ["interrogativa_total"]

		if not verbo_neg_irregular and palavra.upper() != "MUITO":
			i.traducao_palavras.append(palavra.upper().replace("_", " ").replace("-", " ").replace(" DE", ""))
	

		# remove o adverbio de intensidade MUITO
		if palavra.upper() == "MUITO":
			del i.traducao[indice]
			indice -= 1		

		#coverte gestos compostos
		print("GESTOS COMPOSTOSSS")
		print(gestos_compostos)
		if palavra.upper() in gestos_compostos:
			del i.traducao[indice]
			for index, value in enumerate(gestos_compostos[palavra.upper()]):
				if (index > 0):
					classe += "_COMP"
				i.traducao.insert(indice, (palavra, value, classe))
				indice += 1

		indice += 1

def converte_glosas(i, counter):
	"""
	Converte as palavras em glosas.
	:param traducao: frase
	:return:
	"""
	verbo_neg_irregular = False
	adverbio_negacao =  False
	indice = 0
	gest_comp_frase = [False] * len(i.traducao)
	while indice < len(i.traducao):
		valor = i.traducao[indice]
	# for indice, valor in enumerate(i.traducao):
		classe = valor[2]
		lema = valor[1]
		palavra = valor[0]
		# Se não tiver um quantificador numeral então faz-se o plural
		if (classe.startswith("NC") and classe[3] == "P") or (classe.startswith("AQ") and classe[4] == "P") and "NUM" not in i.classes:
			i.traducao[indice] = palavra.upper()
		else:
			i.traducao[indice] = lema.upper()

		# if not classe.startswith("A") and not classe.startswith("NC"):
		# 	i.traducao[indice] = lema.upper()

		# else:
		# 	i.traducao[indice] = palavra.upper()

		if classe.startswith("Z"):
			try:
				int(palavra)
			except ValueError:
				# Transforma numeros por exenso sem ser por extenso
				i.traducao[indice] = str(ExtensoToInteiro(palavra))
	
		print(palavra)
		
		if "COMP" in classe:
			gest_comp_frase[indice] = True

		print(gest_comp_frase)			

		indice += 1
	
	return gest_comp_frase

		# Adiciona a expressao negativa no gesto manual NÃO
		# if classe.startswith("RN") and "NEG" in i.tipo[0]:
		# 	exprFaciais[str(indice+counter) + "-" + str(indice+counter+1)] = "negativa"

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

def geracao(i, counter, exprFaciais, negativa_irregular, gestos_compostos):
	"""
	Função principal que aplica as regras manuais anteriores conforme a gramática da LGP.
	:param i: Frase em português (objeto).
	:return: Frase em LGP
	"""

	classes = list(list(zip(*i.traducao))[2])

	# remover "ser", "estar" e "e"
	remove_ser_estar(i.traducao)

	# remover preposições
	remove_prep(i.traducao)

	#altera ordem determinantes, numerais e adverbios quantidade
	ordena_dets_num_adverq(i.traducao)

	#feminino
	excepcoes = abre_feminino_excepcoes()
	feminino(i.traducao, excepcoes)

	#nomes próprios
	# nomes_proprios(i.traducao, i.palavras_compostas)
	
	# transformar cliticos
	cliticos(i.traducao)

	print(i.traducao)

	#advérbio de negação para o fim da oração
	orden_neg(i, counter, exprFaciais, negativa_irregular)

	#interrogativas parciais (pronomes e advérbios) para o fim da oração
	orden_int(i, counter, exprFaciais, negativa_irregular)

	print(i.traducao)

	#Verbos
	tempo_verbal(i)

	print(i.traducao)

	# adicionar expressão facial negativa e interrogativa, e converte gestos_compostos
	expressoes_faciais(i, counter, exprFaciais, negativa_irregular, gestos_compostos)

	print("expreeeee: ")
	print(i.traducao)

	# passar para glosas, identifica gestos compostos
	gest_comp_frase = converte_glosas(i, counter)
	print("GESTOS COMPOSTOS:")
	print(gest_comp_frase)

	print(i.traducao)

	# join das glosas da traducao
	traducao_glosas = " ".join(i.traducao)

	# print(i.traducao)

	traducao_glosas = traducao_glosas.split(" ")

	# adicionar a expressao "olhos franzidos" à frase toda se for uma interrogativa e/ou negativa
	expressao_olhos_franzidos(i.tipo, traducao_glosas, counter, exprFaciais)

	return list(filter(None, traducao_glosas)), exprFaciais, " ".join(i.traducao_palavras), gest_comp_frase
