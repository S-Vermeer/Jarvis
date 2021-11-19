import wolframalpha as wa

app_id = 'QW82JW-Q5U44TYEE9'  # get your own at https://products.wolframalpha.com/api/

def connect_wa():
    client = wa.Client(app_id)
    return client