import json
from json import JSONEncoder

import numpy as np


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def numpy_encoder(func):
    def wrapper(*args, **kwargs):
        return json.loads(
            json.dumps(func(*args, **kwargs), cls=NumpyArrayEncoder))
    return wrapper
