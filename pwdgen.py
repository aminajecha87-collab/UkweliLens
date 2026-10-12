import random
import string


def generate_password(length=12, use_upper=True, use_numbers=True, use_special=True):
    """===WELCOME PASSWORD GENERATION====Generates a secure, random password based on user preferences."""
    # Always include lowercase letters as the base requirement
    characters = string.ascii_lowercase

    # Add uppercase letters if selected
    if use_upper:
        characters += string.ascii_uppercase

    # Add digits if selected
    if use_numbers:
        characters += string.digits

    # Add special punctuation characters if selected
    if use_special:
        characters += string.punctuation

    # Randomly select characters from the pool for the specified length
    password = "".join(random.choice(characters) for _ in range(length))

    return password


# Example usage:
if __name__ == "__main__":
    # Create a 16-character password with all character types enabled
    new_password = generate_password(
        length=16, use_upper=True, use_numbers=True, use_special=True
    )

    # Display the generated password to the user
    print(f"Generated Password: {new_password}")

