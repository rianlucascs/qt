

def writing(path, message):
    with open(path, 'a', encoding='utf-8') as file:
        file.write(message)
    return None