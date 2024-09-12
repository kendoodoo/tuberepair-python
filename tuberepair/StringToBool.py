def StringToBool(input):
    if not isinstance(input, str):
        raise ValueError("A String was not passed")
    lowerInput = input.lower()
    if lowerInput == "true":
        return True
    elif lowerInput == "false":
        return False
    raise ValueError("This string isn't true of false!")