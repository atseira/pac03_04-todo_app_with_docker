import secrets

SECRET_KEY = secrets.token_hex(16)  # generates a random hex token of 256-bits (32 bytes)
print(SECRET_KEY)

# copy paste the printed SECRET_KEY to .env_example and rename it to .env