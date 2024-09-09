"""

Blocklist for JWT tokens
This file just contains the blocklist for JWT tokens. It will be imported by app and the logout
resource so that tokens can be added to the blocklist upon logout.

"""
# You may want to store the BLOCKLIST in a database. You can use redis for maximum performance. This can be a further exercise
BLOCKLIST = set()