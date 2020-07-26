from twilio.rest import Client

account_sid = "ACe116637ceaee25821e317dd0ddf8230c"
auth_token = "bb750ab98047a4ea7fcbf6822a55ebe4"

client = Client(account_sid, auth_token)

client.api.account.messages.create(
    to="+96598585924",
    from_="+12056228969",
    body="السلام عليكم")

