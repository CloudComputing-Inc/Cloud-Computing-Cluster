#test auth0
import http.client

conn = http.client.HTTPSConnection("dev-h2k5uttlw0fkxdod.us.auth0.com")

payload = "{\"client_id\":\"jEsdI0mibeppkf9H6CdiR77TTj8TR86o\",\"client_secret\":\"zxJ86PVfHFr957Cx7hRH33iG0Vs_JtA0Dp-BZpgQWkhVdkvvk_vwDx2hmgOLeaMY\",\"audience\":\"https:\\amazon-reviews.net\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))