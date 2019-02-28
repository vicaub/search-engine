# Vectoriel avec tf_idf
import re

from tokenization import read_forbidden_words

forbidden_words = read_forbidden_words()


def get_list_term_id_from_request(request, dict_term):
    list_term_id = []
    if len(request) > 0:
        tokens = re.compile("[^0-9a-zA-Z]").split(request)
        for token in tokens:
            if token.lower() not in forbidden_words and len(token) > 0:
                if token.lower() not in forbidden_words and token.lower() in dict_term:
                    list_term_id.append(dict_term[token.lower()])
    return list_term_id


def get_dft_list(inverse_index_filename):
    """
    dft: nombre de documents contenant le terme t
    """
    with open(inverse_index_filename) as f:
        dft = []
        for line in f.readlines():
            splitted_line = line.split()
            frequency = len(splitted_line) - 1
            dft.append(frequency)
    return dft


def get_posting_lists(term_ID_list, inverse_index_filename):
    with open(inverse_index_filename) as f:
        posting_lists = {}
        for line in f.readlines():
            splitted_line = line.split()
            term_id = int(splitted_line[0])
            if term_id in term_ID_list:
                posting_list = {}
                for k in range(1, len(splitted_line)):
                    doc_id, freq = map(int, splitted_line[k].split(","))
                    posting_list[doc_id] = freq
                posting_lists[term_id] = posting_list
    return posting_lists


def get_document_list_from_postig_lists(posting_lists):
    docs = set()
    for posting_list in posting_lists.values():
        for d in posting_list.keys():
            docs.add(d)
    return list(docs)


def w(t, d, posting_lists, dfts, N):
    if t not in posting_lists:
        return 0
    if d in posting_lists[t]:
        tftd = posting_lists[t][d]
    else:
        return 0
    dft = dfts[t]
    tf = (1 + log(tftd, 10))
    idf = log(N / dft, 10)

    return tf * idf


# compute_normalization_coeff_memory = {}


def compute_normalization_coeff(d, posting_lists, dfts, N, dict_term):
    # if (d, str(posting_lists), str(dfts), N) in compute_normalization_coeff_memory:
    #     return compute_normalization_coeff_memory[(d, str(posting_lists), str(dfts), N)]
    # else:
    s = 0
    for term_id in dict_term.values():
        s += w(term_id, d, posting_lists, dfts, N)
        # compute_normalization_coeff_memory[(d, str(posting_lists), str(dfts), N)] = sqrt(s)
    return sqrt(s)


def w_normalized(t, d, posting_lists, dfts, N, dict_term):
    if d in posting_lists[t]:
        tftd = posting_lists[t][d]
    else:
        return 0
    dft = dfts[t]
    tf = (1 + log(tftd, 10))
    idf = log(N / dft, 10)
    norm = compute_normalization_coeff(d, posting_lists, dfts, N, dict_term)
    if tf > 1:
        return 1 + log(tf) * idf * (1 / norm)
    else:
        return 0


def normalized_frequency(t, d, posting_lists, dfts, N, dict_term):
    if d in posting_lists[t]:
        tftd = posting_lists[t][d]
    else:
        return 0
    dft = dfts[t]
    # calcul des tf
    tf = (1 + log(tftd, 10))
    tf_maxi = 0
    for term_id in dict_term.values():
        if term_id in posting_lists:
            tftd_tid = posting_lists[t][d]
            tf_tid = (1 + log(tftd_tid, 10))
            if tf_tid > tf_maxi:
                tf_maxi = tf_tid
    return tf / tf_maxi


def vectorize_request(list_term_id, N, dfts):
    vector_request = []
    for term_id in list_term_id:
        vector_request.append(log(N / dfts[term_id], 10))
    return vector_request


def vectorize_document(doc_id, list_term_id, N, dfts, posting_lists, ponderation, dict_term):
    vector_doc = []
    for term in list_term_id:
        if ponderation == "tfidf":
            vector_doc.append(w(term, doc_id, posting_lists, dfts, N))
        elif ponderation == "tfidf_norm":
            vector_doc.append(w_normalized(term, doc_id, posting_lists, dfts, N, dict_term))
        elif ponderation == "norm_freq":
            vector_doc.append(normalized_frequency(term, doc_id, posting_lists, dfts, N, dict_term))

    return vector_doc


from math import sqrt, log


def find_nearest_cosinus_vector(vector_request, vector_doc_list):
    minimum = float('inf')
    minimum_ind = 0
    for doc_id, vector_doc in vector_doc_list.items():
        produit_scalaire = 0
        norme_1 = 0
        norme_2 = 0
        for i in range(len(vector_request)):
            produit_scalaire += vector_request[i] * vector_doc[i]
            norme_1 += vector_request[i] ** 2
            norme_2 += vector_doc[i] ** 2
        if norme_2 == 0:
            mesure = float('inf')
        else:
            mesure = produit_scalaire / (sqrt(norme_1) * sqrt(norme_2))
        if mesure <= minimum:
            minimum = mesure
            minimum_ind = doc_id
    return minimum_ind


def modele_vectoriel(request, documents, dict_terms, ponderation="tfidf", type="CACM"):
    compute_normalization_coeff_memory = {}
    docs = documents
    N = len(documents)

    dfts = get_dft_list("frequential_index/" + type.lower() + "/" + type.lower() + ".output")

    list_term_id = get_list_term_id_from_request(request, dict_terms)
    posting_lists = get_posting_lists(list_term_id,
                                      "frequential_index/" + type.lower() + "/" + type.lower() + ".output")
    docs = get_document_list_from_postig_lists(posting_lists)

    vector_doc_list = {}
    for doc in docs:
        vector_doc_list[doc] = vectorize_document(doc, list_term_id, N, dfts, posting_lists, ponderation, dict_terms)

    vector_request = vectorize_request(list_term_id, N, dfts)

    best_vector_docs = []

    while len(vector_doc_list) > 0:
        best_doc = find_nearest_cosinus_vector(vector_request, vector_doc_list)
        best_vector_docs.append(best_doc)
        vector_doc_list.pop(best_doc, None)

    return best_vector_docs
