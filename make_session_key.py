import random

def generate_session_key(key_len):
    chars_dict = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM~!@#$%^&*()_+|}{:?><[];.,=")
    session_key = ""
    for i in range(key_len):
        session_key = session_key + chars_dict[random.randint(0, len(chars_dict) - 1)]
    return session_key