def exchange_model(command):
    if command and command.startswith("환율"):
        return "exchange"
    return None
