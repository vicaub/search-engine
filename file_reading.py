import os

def read_cacm():
    """
    :return: array of documents represented by [title, abstract, content]
    """
    file_name = "./Data/CACM/cacm.all"
    file = open(file_name)
    documents = []
    current_section = -1
    for line in file.readlines():
        if line[0] == '.':
            if line[1] == 'I':
                documents.append(["", "", ""])
            elif line[1] == 'T':
                current_section = 0
            elif line[1] == 'W':
                current_section = 1
            elif line[1] == 'K':
                current_section = 2
            else:
                current_section = -1
        else:
            if current_section >= 0:
                if len(documents[-1][current_section]) == 0:
                    # adding information in section
                    documents[-1][current_section] += line.strip('\n')
                else:
                    documents[-1][current_section] += " " + line.strip('\n')
    file.close()
    return documents


def read_cs276():
    """
    returns list for document tokens
    """
    collection_path = "./Data/CS276/pa1-data/"
    documents = []

    # getting all sub folders which are not hidden
    sub_dirs = [collection_path + path + "/" for path in os.listdir(collection_path) if path[0] != "."]

    for sub_path in sub_dirs:
        for article in os.listdir(sub_path):
            if article[0] != ".":  # check if it's not a hidden file
                with open(sub_path + article) as f:
                    documents.append(f.read().strip().split())

    return documents
