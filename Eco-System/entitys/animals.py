























import inspect, sys
def get_classes():
    return inspect.getmembers(sys.modules[__name__], inspect.isclass)