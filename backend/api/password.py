from bcrypt import hashpw, gensalt, checkpw

# Hashing a password
password = "my_secure_password"
hashed_password = hashpw(password.encode(), gensalt())

# print(password)
# print(password.encode())
# print(hashed_password)

password = "my_secure_password!"

# Compare to stored hash
if checkpw(password.encode(), hashed_password):
    print("Password matches!")
else:
    print("Invalid password.")
