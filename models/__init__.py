def exchange_model(command):
    if command and command.startswith("환율"):
        return "exchange"
    return None


def coin_model(command):
    if command and command.startswith("coin"):
        return "coin"
    return None
