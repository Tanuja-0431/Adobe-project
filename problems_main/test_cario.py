try:
    import cairo
    print("cairo is installed correctly.")
except ImportError as e:
    print("cairo is not installed.")
    print(e)
