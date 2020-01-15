# log error to console, or file

errors = []


# persist and print error message
def log_error(error):
    errors.append(error)
    print(error)
