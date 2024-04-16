import http.client

conn = http.client.HTTPSConnection("")

payload = "grant_type=client_credentials&client_id=AIkuRjPztTwZRI0koapVkutbI2L3ZP3Z&client_secret=-zmKEpkZe8lL_S_7DZbTVZJmySZQsE3Jpa1vOI6X2OCsjjS89dLnT9QzKprUZMGG&audience=YOUR_API_IDENTIFIER"

headers = { 'content-type': "application/x-www-form-urlencoded" }

conn.request("POST", "/dev-h2k5uttlw0fkxdod.us.auth0.com/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))



import http.client

conn = http.client.HTTPSConnection("myapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "Bearer ACCESS_TOKEN"
    }

conn.request("GET", "/api", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))