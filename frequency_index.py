import tokenization


def write_dict_with_frequency(file_name, liste):
    f = open(file_name, "w")
    for termId, list_docID in liste:
        f.write(str(termId))
        f.write(" ")
        for docID in list_docID:
            f.write(str(docID[0]) + "," + str(docID[1]) + " ")
        f.write("\n")
    f.close()


def read_line_with_frequency(line):
    nombres = line.split(' ')
    nombres.pop()  # on enlève le \n
    termID = int(nombres[0])
    list_docID = []
    for couple in nombres[1:]:
        docID, freq = map(int, couple.split(","))
        list_docID.append([docID, freq])
    return (termID, list_docID)


def add_token_to_term_list_with_frequency(term_list, token, new_list_docID, dict_term):
    new_termID = dict_term[token]
    for termID, list_docID in term_list:
        if termID == new_termID:
            for docID in new_list_docID:
                deja_present = False
                for old_docID, freq in list_docID:
                    if docID == old_docID:
                        freq += 1
                        deja_present = True
                        break
                if not deja_present:
                    list_docID.append([docID, 1])
            return
    docID_with_freq = []
    for docID in new_list_docID:
        if docID not in [x[0] for x in docID_with_freq]:
            docID_with_freq.append([docID, new_list_docID.count(docID)])
    term_list.append((new_termID, docID_with_freq))  # On enlève les doublons


def invert_block_with_frequency_CACM(documents, indice_premier, taille, dict_term):
    tokens = tokenization.tokenize_no_nltk_CACM(documents[indice_premier:indice_premier + taille])
    index_inverse_block = []
    for token, list_docID in tokens.items():
        add_token_to_term_list_with_frequency(index_inverse_block, token,
                                              [docID + indice_premier for docID in list_docID], dict_term)
    return index_inverse_block

def invert_block_with_frequency_CS276(documents, indice_premier, taille, dict_term):
    tokens = tokenization.tokenize_CS276(documents[indice_premier:indice_premier + taille])
    index_inverse_block = []
    for token, list_docID in tokens.items():
        add_token_to_term_list_with_frequency(index_inverse_block, token,
                                              [docID + indice_premier for docID in list_docID], dict_term)
    return index_inverse_block


def trouver_terme_mini_with_frequency(liste_lignes):
    minimum = float('inf')
    min_indices = []
    for i in range(len(liste_lignes)):
        if liste_lignes[i] != "":
            termID = read_line_with_frequency(liste_lignes[i])[0]
            if termID < minimum:
                minimum = termID
                min_indices = [i]
            elif termID == minimum:
                min_indices.append(i)
    return min_indices


def index_inverse_global_with_frequency(documents, taille, file_name, dict_term, type="CACM"):
    indice = 0
    n = 0
    while indice < len(documents):
        if indice % 1000 == 0:
            print("Processing document {}/{}          ".format(str(indice), str(len(documents))), end="\r")
        if type == "CACM":
            index_inverse_block = invert_block_with_frequency_CACM(documents, indice, taille, dict_term)
        elif type == "CS276":
            index_inverse_block = invert_block_with_frequency_CS276(documents, indice, taille, dict_term)

        index_inverse_block.sort(key=lambda x: x[0])

        write_dict_with_frequency(file_name + "_" + str(n), index_inverse_block)
        n += 1
        indice += taille
    files = [open(file_name + "_" + str(i)) for i in range(n)]
    lignes_courantes = [files[i].readline() for i in range(n)]
    blocks_finis = 0
    final_dict = open(file_name, "w")
    while blocks_finis < n:
        min_indices = trouver_terme_mini_with_frequency(lignes_courantes)
        termID = read_line_with_frequency(lignes_courantes[min_indices[0]])[0]
        docIDs = []
        for i in min_indices:
            docIDs += read_line_with_frequency(lignes_courantes[i])[1]
        final_dict.write(str(termID))
        final_dict.write(" ")
        for docID in docIDs:
            final_dict.write(str(docID[0]) + "," + str(docID[1]) + " ")
        final_dict.write("\n")
        for i in min_indices:
            lignes_courantes[i] = files[i].readline()
            if lignes_courantes[i] == '':
                blocks_finis += 1
    [files[i].close() for i in range(n)]
    final_dict.close()
