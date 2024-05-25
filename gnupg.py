import gnupg


# Initialize GPG
def initialize_gpg():
    return gnupg.GPG()


# Generate a new key
def generate_key(gpg, key_type="RSA", key_length=2048, name_email="user@example.com"):
    input_data = gpg.gen_key_input(
        key_type=key_type,
        key_length=key_length,
        name_email=name_email
    )
    key = gpg.gen_key(input_data)
    return key


# Rotate keys (generate a new key and delete the old one)
def rotate_key(gpg, old_key_fingerprint, key_type="RSA", key_length=2048, name_email="user@example.com"):
    # Generate a new key
    new_key = generate_key(gpg, key_type, key_length, name_email)

    # Delete the old key
    delete_key(gpg, old_key_fingerprint)

    return new_key


# Delete a key by its fingerprint
def delete_key(gpg, key_fingerprint):
    # Delete the secret key
    gpg.delete_keys(key_fingerprint, True)
    # Delete the public key
    gpg.delete_keys(key_fingerprint)


# Main execution
if __name__ == "__main__":
    try:
        # Initialize GPG
        gpg = initialize_gpg()

        # Generate a new key
        print("Generating a new key...")
        new_key = generate_key(gpg)
        print(f"Generated key fingerprint: {new_key.fingerprint}")

        # Rotate the key (this will generate a new key and delete the old one)
        print("Rotating the key...")
        rotated_key = rotate_key(gpg, new_key.fingerprint)
        print(f"Rotated key fingerprint: {rotated_key.fingerprint}")

        # Destroy the rotated key
        print("Destroying the rotated key...")
        delete_key(gpg, rotated_key.fingerprint)
        print("Rotated key destroyed.")

    except AttributeError as e:
        print("Error: ", e)
