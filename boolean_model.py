from tokenization import read_forbidden_words


def shunting_yard(query):
    """Transforms an infix query with & | ! into an inverse polish notation"""
    n = len(query)
    i = 0
    output = []
    stack = []
    while i < n:
        if query[i].isalnum():
            mot = ""
            while i < n and query[i].isalnum():
                mot += query[i]
                i += 1
            i -= 1
            output.append(mot)
        elif query[i] in "!&|":
            stack.append(query[i])
        elif query[i] == '(':
            stack.append(query[i])
        elif query[i] == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            raise Exception("Problème de parsing")
        i += 1
    while len(stack) > 0:
        output.append(stack.pop())

    return output


def find_documents_from_term(term, dict_term, type):
    """
    return the documents containing term from inversed index
    """
    if term not in dict_term:
        return set()
    else:
        termID = dict_term[term]
        with open("inversed_index/" + type.lower() + "/" + type.lower() + ".output") as f:
            lines = f.readlines()
        for line in lines:
            splited_line = line.strip().split(" ")
            if splited_line[0] == str(termID):
                # print(set(splited_line[1:]))
                return set(splited_line[1:])


stop_list = read_forbidden_words()


def find_documents(polish_notation, documents, dict_term, type):
    stack = []
    all_docs = set(range(len(documents)))
    for token in polish_notation:
        if token.isalpha():
            if token.lower() in stop_list:
                stack.append("stop")
            else:
                stack.append(find_documents_from_term(token.lower(), dict_term, type))
        elif token == "|":
            value1 = stack.pop()
            value2 = stack.pop()
            if value1 == "stop":
                stack.append(value2)
            elif value2 == "stop":
                stack.append(value1)
            else:
                stack.append(value1 | value2)
        elif token == "&":
            value1 = stack.pop()
            value2 = stack.pop()
            if value1 == "stop":
                stack.append(value2)
            elif value2 == "stop":
                stack.append(value1)
            else:
                stack.append(value1 & value2)
        elif token == "!":
            value = stack.pop()
            if value == "stop":
                stack.append("stop")
            else:
                stack.append(all_docs - value)

    return stack.pop()


def boolean_model(query, documents, dict_term, type):
    polish_notation = shunting_yard(query)
    return find_documents(polish_notation, documents, dict_term, type)


if __name__ == "__main__":
    test = "(a&!b)|(c|terme)"
    print(shunting_yard(test))
