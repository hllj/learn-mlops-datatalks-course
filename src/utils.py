import pickle


def dump_pickle(obj, filename):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)
    
def load_pickle(filename: str):
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data