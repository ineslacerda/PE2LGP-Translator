from Frase_input import Frase_input
import sys
sys.path.append('../Modulo_construcao_regras')
import freeling
from dependencias import dependencies_spacy
from elementos_sintaticos import set_elementos
from identifica_suj_pred import identifica_elementos
import re


def retirar_pontuacao(pred_tags):
	pred = []
	indices = []
	for indx, val in enumerate(pred_tags):
		if not val.startswith("F"):
			pred.append(val)
		else:
			indices.append(indx)
	return pred, indices



def retirar_determinante(pred_tags, words):
	ind = []

	for indx, val in enumerate(pred_tags):
		if val.startswith("DA") or (val.startswith("DI") and (words[indx].lower() == "um" or words[indx].lower() == "uma")):
				ind.append(indx)

	for i in sorted(ind, reverse=True) :
		del pred_tags[i]


	return ind


def tipo_de_frase(pred_tags, pont):
	"""
	Identifica o tipo da frase.
	:param pred_tags: lista com as etiquetas morfossintáticas
	:param pont: sinal de pontuação
	:return: lista com o tipo da frase
	"""
	tipo_frase = []
	if pont == "!" and "RN" not in pred_tags:
		tipo_frase.append("EXCL")

	elif pont == "?" and "RN" not in pred_tags:
		tipo_frase.append("INT")

	elif "RN" in pred_tags and pont =="!":
		tipo_frase.append("NEG")
		tipo_frase.append("EXCL")

	elif "RN" in pred_tags and pont =="?":
		tipo_frase.append("INT")
		tipo_frase.append("NEG")

	elif "RN" in pred_tags:
		tipo_frase.append("NEG")

	else:
		tipo_frase.append("CAN")

	return tipo_frase


def converte_estrutura(anotacao, dic):
	"""
	Converte as etiquetas de dependencias para as do corpus.
	:param anotacao: Lista com as etiquetas de dependências.
	:param dic: Dicionário com as correspondências entre as etiquetas e as do corpus.
	:return: Lista com as relações de dependências de acordo com as etiquetas do corpus.
	"""
	convertido =[]

	for a in anotacao:
		if a.lower() in dic.keys() and dic[a.lower()] not in convertido:
			convertido.append(dic[a.lower()])

	return convertido

def converte_classes(frase, map_corpus_tags):
	"""
	Converte as etiquetas morfossintáticas para as do Corpus.
	:param frase: lista com as etiquetas morfossintáticas
	:param map_corpus_tags: Dicionário com o mapeamento entre as etiquetas morfossintáticas e as do Corpus.
	:return: Lista de etiquetas morfossintáticas de acordo com as notações do Corpus.
	"""
	novas_classes = []
	for c in frase:
		for v in map_corpus_tags.keys():
			if c.startswith(v):
				novas_classes.append((map_corpus_tags[v]))
				frase[frase.index(c)] = map_corpus_tags[v]

	return novas_classes

def atualiza_listas(lista, indices):
	for l in sorted(indices, reverse=True):
		del lista[l]


def palavra_composta(words):
	"""
	Identifica as palavras compostas, separadas por um hífen.
	:param words: Lista com as palavras da frase em português.
	:return: Lista com as palavras compostas e a lista com os seus indices na frase em português.
	"""
	palavras_compostas = []
	indices = []
	for w in range(len(words)):  # Para os casos em que as palavras são compostas
		palavras = words.copy()
		if "_" in words[w]:
			palavras_compostas.append(palavras[w])
			words[w] = words[w].replace("_", "")
			indices.append(w)

	return palavras_compostas, indices

def atualiza_tags(adv_quant, words, pred_tags, sub):
	"""
	Atualiza as etiquetas de advérbios e pronomes com os seus subtipos.
	:param adv_quant: string, advérbio
	:param words: lista com as palavras da frase
	:param pred_tags: lista com as etiquetas morfossintaticas das palavras
	:param sub: etiqueta a substituir
	:return:
	"""
	for adv in adv_quant:

		advs = list(filter(lambda x: adv.lower() == x[1].lower(), enumerate(words)))
		if advs and pred_tags[words.index(advs[0][1])].startswith("RG"):
			pred_tags[words.index(advs[0][1])] = sub

		if advs and pred_tags[words.index(advs[0][1])].startswith("PR"):
			pred_tags[words.index(advs[0][1])] = sub


def obj_verb_transitivo(pred_tags, dep_tags):
	verbs = list(filter(lambda x: pred_tags[x[0]].startswith("V") and dep_tags[x[0]] == "ROOT" and dep_tags[x[0]+1] == "case", enumerate(dep_tags)))

	objs_verbs_trans = {}
	for verb in verbs:
		objs_verbs_trans[str(verb[0]+3)] = dep_tags[verb[0]+3]

	return objs_verbs_trans


def preprocessar(f, freeling_values):
	"""
	Realiza a análise sintática e morfossintática da frase em português.
	:param f: string, frase em português.
	:param freeling_values: parâmetros da ferramenta Freeling
	:return: objeto da classe Frase_input com as caracteristicas gramaticais da frase em português
	"""

	map_corpus_dep = {'root': 'V', 'nsubj': 'S', 'obj': 'O', 'obl': 'O', 'iobj': 'O'}
	map_corpus_tags = {'R': 'ADV', 'A': 'ADJ', 'CS': 'CONJ', 'D': 'DET', 'N':'N', 'S':'PREP', 'P':'PRON', 'V':'V', 'Z': 'NUM', 'CC': 'CONJ' }

	# 1º estrutura frásica:
	# dep_words, dep_tags, indices_filhos = dependencies_spacy(f, freeling_values)


	# 2º constituintes com Freeling
	words, lemmas, lemma_verdadeiro, pred_tags = freeling.main(f, freeling_values)

	print("words")
	print(words)
	print("lemmas")
	print(lemmas)
	print("lemma_verdadeiro")
	print(lemma_verdadeiro)
	print("pred_tags")
	print(pred_tags)

	# palavras_compostas, indices_compostas = palavra_composta(words)


	adv_quant = ["muito", "muitos", "muita", "muitas", "menos", "tanto", "pouco", "pouca", "demasiado", "bastante", "apenas", "mais", "tanto"]
	adv_temporal = ["fim_de_semana"]
	adv_tempo_passado = ['ontem', 'outrora', 'dantes', 'antigamente', 'antes', 'já', 'hoje_de_manhã']
	adv_tempo_futuro = ['logo', 'amanhã', 'doravante','em_breve']
	adv_int = ["onde", "quando", "como", "porque"]
	pronomes_int = ["qual", "quais", "quantos", "quantas", "quanto", "porquê", "quem"]
	adv_neg = ["nunca"]

	atualiza_tags(adv_quant, words, pred_tags, "RGQ")
	atualiza_tags(adv_temporal, words, pred_tags, "RGT")
	atualiza_tags(adv_tempo_passado, words, pred_tags, "RGTP")
	atualiza_tags(adv_tempo_futuro, words, pred_tags, "RGTF")
	if f[-1] == "?": #atualiza pronomes/advérbios interrogativos se for uma interrogativa
		atualiza_tags(pronomes_int, words, pred_tags, "PT")
		atualiza_tags(adv_int, words, pred_tags, "RGI")
	atualiza_tags(adv_neg, words, pred_tags, "NEGA")

	print(words)

	print(pred_tags)

	sub_frases_words = []
	sub_frases_lemmas = []
	sub_frases_lemma_verdadeiro = []
	sub_frases_pred_tags = []
	index  = 0

	delimiters = []
	string_delimiters = ""
	
	for m, i in enumerate(pred_tags):
		if i.startswith("PE") and words[m].lower() in pronomes_int:
			pred_tags[m] = "PT"

		# adverbio de negação --> ainda não
		if i == "RG" and pred_tags[m+1] == "RN":
			pred_tags[m] = "NEGA"
			words[m] = "ainda_não"
			lemmas[m] = "ainda_não"
			lemma_verdadeiro[m] = "ainda_não"
			i = "NEGA"
		# a estrutura das interrogativas tem que ser preservada
		if (i == "Fc" or i == "CC" or i == "CS" or i == "RG") and f[-1] != "?": #só separa em orações se não for uma interrogativa
			sub_frases_words.append(words[index:m])
			sub_frases_lemmas.append(lemmas[index:m])
			sub_frases_lemma_verdadeiro.append(lemma_verdadeiro[index:m])
			sub_frases_pred_tags.append(pred_tags[index:m])
			#adicionar conjunção em separado se não for uma virgula
			if words[m] != ",":
				sub_frases_words.append([words[m]])
				sub_frases_lemmas.append([lemmas[m]])
				sub_frases_lemma_verdadeiro.append([lemma_verdadeiro[m]])
				sub_frases_pred_tags.append([pred_tags[m]])

			delimiters.append(words[m])
			if m == index:	
				string_delimiters += words[m] + " |"
			else:
				string_delimiters += " " + words[m] + " |"

			index = m + 1

	string_delimiters = string_delimiters[0:len(string_delimiters)-1]

	sub_frases_words.append(words[index:len(words)])
	sub_frases_pred_tags.append(pred_tags[index:len(words)])
	sub_frases_lemmas.append(lemmas[index:len(lemmas)])
	sub_frases_lemma_verdadeiro.append(lemma_verdadeiro[index:len(lemma_verdadeiro)])

	sub_frases_words = list(filter(None, sub_frases_words))
	sub_frases_pred_tags = list(filter(None, sub_frases_pred_tags))
	sub_frases_lemmas = list(filter(None, sub_frases_lemmas))
	sub_frases_lemma_verdadeiro = list(filter(None, sub_frases_lemma_verdadeiro))

	print(sub_frases_words)
	frase = []
	print(string_delimiters)
	if f[-1] != "?" and delimiters: # só divide em orações se frase não for interrogativa
		frase = re.split(string_delimiters, f)
		print(frase)
		indice = 0
		index = 0
		while indice < len(frase)-1:
			print(index)
			if delimiters[index] != ",":
				frase.insert(indice+1, delimiters[index])
				indice += 1
			indice += 1
			index += 1
			# frase[index+1] = value + " " + frase[index+1]
	else:
		frase.append(f)

	frase = list(filter(None, frase))

	print(frase)

	
	frases = []
	for index in range(0, len(sub_frases_words)):

		print(sub_frases_words[index])

		dep_words, dep_tags, indices_filhos = dependencies_spacy(frase[index], freeling_values)

		print("dependency tagsss")
		print(dep_words)
		print(dep_tags)
		print(indices_filhos)

		frase_input = Frase_input(frase[index])

		#verb_trans_obj

		# for p in palavras_compostas:
		# 	for k in indices_compostas:
		# 		frase_input.set_palavras_compostas(sub_frases[index][k], p)

		sub_frases_pred_tags[index], indx_remo = retirar_pontuacao(sub_frases_pred_tags[index])

		atualiza_listas(sub_frases_words[index], indx_remo)

		# Guarda indice do objecto de um verbo transitivo
		frase_input.obj_verb_trans = obj_verb_transitivo(sub_frases_pred_tags[index], dep_tags)

		# modifica dep_tags
		dependencies_tags = identifica_elementos(dep_tags, indices_filhos)

		frase_input.set_dep_tags(dependencies_tags)

		ind_eliminado = retirar_determinante(sub_frases_pred_tags[index], sub_frases_words[index])

		atualiza_listas(dependencies_tags, ind_eliminado)
		atualiza_listas(sub_frases_lemmas[index], indx_remo)
		atualiza_listas(sub_frases_lemmas[index], ind_eliminado)

		frase_input.set_lemmas_sem_det(sub_frases_lemmas[index])

		atualiza_listas(sub_frases_lemma_verdadeiro[index], ind_eliminado)

		frase_input.set_lemma_verdade_sem_det(sub_frases_lemma_verdadeiro[index])

		# 3º identificar o tipo de frase
		tipo = tipo_de_frase(sub_frases_pred_tags[index], frase[index][-1])
		frase_input.set_tipo(tipo)

		pred_tags_antes = sub_frases_pred_tags[index].copy()
		frase_input.set_classes_antes(pred_tags_antes) #Lista com as palavras todas da frase (ex: com determinantes artigos)

		# 4º retirar em cada elemento o determinantes artigos
		dependency_pt = list(filter(lambda a: a != 'punct', dep_tags))

		atualiza_listas(dep_words, ind_eliminado)
		atualiza_listas(dependency_pt, ind_eliminado)
		frase_input.set_palavras(dep_words)
		frase_input.set_frase_sem_det(dep_words, sub_frases_lemmas[index], pred_tags_antes)
		frase_input.set_frase_sem_det_lemmas_verd(dep_words, lemma_verdadeiro, pred_tags_antes)

		# 5º identificar o que é suj, obj, verbo e predicado
		set_elementos(dependencies_tags, sub_frases_pred_tags[index], dep_words, frase_input)

		# 6º converter as etiquetas de dependenciaa para as do corpus
		estrutura = converte_estrutura(dependencies_tags, map_corpus_dep)
		frase_input.set_dep(estrutura)

		# 7º converter as etiquetas das classes gramaticais para as do corpus
		frase_input.set_classes(sub_frases_pred_tags[index])
		frase_input.set_classes(converte_classes(frase_input.classes, map_corpus_tags) + tipo)
		converte_classes(frase_input.classes_suj, map_corpus_tags)
		converte_classes(frase_input.classes_obj, map_corpus_tags)
		converte_classes(frase_input.classes_verbo, map_corpus_tags)
		converte_classes(frase_input.classes_outro, map_corpus_tags)
		converte_classes(frase_input.classes_pred, map_corpus_tags)

		# 8º concatenar às novas classes, o tipo da frase:
		frase_input.set_classes(frase_input.classes + tipo)

		frases.append(frase_input)

	return frases
