def sim(e1,e2, embeddings):
	try:
		valor = embeddings.similarity(e1, e2)
	except:
		valor = 0

	return valor

