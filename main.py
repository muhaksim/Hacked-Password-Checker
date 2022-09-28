import hashlib
import requests

# Get's how many times the password was found


def get_count(response, tail):
    hashes = (line.split(':') for line in response.text.splitlines())
    for hash, count in hashes:
        if hash == tail:
            return count
    return 0

# sends request to an api using the hashed password's first five characters


def check_pass(password):
    encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    head, tail = encrypted_pass[:5], encrypted_pass[5:]
    url = "https://api.pwnedpasswords.com/range/" + head
    response = requests.get(url)
    return get_count(response, tail)


def main():
    with open("pass.txt") as file:
        password = file.readlines()[0]
        with open("pass.txt", mode="w") as file:
            file.write("")
        count = check_pass(password)
        if count:
            print(
                f"Your password was {password} was found {count} times. Please change it ASAP.")
        else:
            print(
                f"Your password {password} was found {count} times. Good job.")
    return "Finished"


if __name__ == "__main__":
    main()
