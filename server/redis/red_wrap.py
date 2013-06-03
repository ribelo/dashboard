
import pickle


def encode_hash(h):
    d = {}
    for key in h.keys():
        value = h.get(key)
        key = pickle.dumps(key)
        value = pickle.dumps(value)
        d[key] = value
    return d


def decode_hash(h):
    d = {}
    for key in h.keys():
        value = h.get(key)
        key = pickle.loads(key)
        value = pickle.loads(value)
        d[key] = value
    return d