def get_maps_key():
    with open('key.txt', 'r') as key_file:
        key = key_file.read()
    return key
