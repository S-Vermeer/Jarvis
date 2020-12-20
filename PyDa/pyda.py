import wolframalpha
app_id = 'QW82JW-Q5U44TYEE9'  # get your own at https://products.wolframalpha.com/api/
client = wolframalpha.Client(app_id)

res = client.query('temperature in Washington, DC on October 3, 2012')

query_url = f"http://api.wolframalpha.com/v2/query?" \
             f"appid={appid}" \
             f"&input={query}" \
             f"&format=plaintext" \
             f"&output=json"

r = requests.get(query_url).json()

data = r["queryresult"]["pods"][0]["subpods"][0]
datasource = ", ".join(data["datasources"]["datasource"])
microsource = data["microsources"]["microsource"]
plaintext = data["plaintext"]

print(f"Result: '{plaintext}' from {datasource} ({microsource}).")


print(next(res.results).plainText)
