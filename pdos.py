#!/usr/bin/env python3
# usage: pdos.py [-h] -u <url> -w <path> [-T <threads>]

import argparse, random, requests, secrets, string, sys, threading


def create_email(wordlist):
    domains = (
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com",
        "verizon.net",
        "att.net",
        "earthlink.net",
        "aol.com",
    )
    with open(wordlist) as f:
        lines = [line.strip().lower() for line in f]
    first = random.choice(lines)
    last = random.choice(lines)
    if bool(random.getrandbits(1)):
        first = chr(random.randint(97, 122))
    username = f"{first}{last}" if bool(random.getrandbits(1)) else f"{first}.{last}"
    if bool(random.getrandbits(1)):
        username = f"{username}{random.randint(0, 9999)}"
    return f"{username}@{random.choice(domains)}"


def create_pass():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    password_length = random.randint(8, 20)
    while True:
        password = ""
        for i in range(password_length):
            password += "".join(secrets.choice(alphabet))
        if (
            any(char in special_chars for char in password)
            and sum(char in digits for char in password) >= 2
        ):
            return password


def pdos(url, wordlist):
    while True:
        username = create_email(wordlist)
        password = create_pass()
        payload = {"username": username, "password": password}
        response = requests.post(url, data=payload)
        print(f"{username} {password}\n{response}")


def main():
    print(
        f"""
▀██▀▀█▄      ▀██   ▄▄█▀▀██    ▄█▀▀▀▄█  
 ██   ██   ▄▄ ██  ▄█▀    ██   ██▄▄  ▀  
 ██▄▄▄█▀ ▄▀  ▀██  ██      ██   ▀▀███▄  
 ██      █▄   ██  ▀█▄     ██ ▄     ▀██ 
▄██▄     ▀█▄▄▀██▄  ▀▀█▄▄▄█▀  █▀▄▄▄▄█▀
⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠚⠉⠉⠀⠀⠀⠉⠙⠓⢦⡀⠀⠀⠀⠀⠀⠀
⠀⣰⠋⠀⣀⣠⣤⣤⣤⡄⠀⣤⠤⠤⢿⣦⠀⠀⠀⠀⠀
⢰⠇⠀⠰⡅⠀⠰⢆⡼⠀⠀⠳⢤⡼⠟⠈⣧⠀⠀⠀⠀
⣼⠀⠀⠀⢉⣉⣉⣩⣤⠤⠤⠤⠶⢶⠒⠀⢸⡄⠀⠀⠀
⣿⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢀⠀⣸⠀⢀⡼⠀⠀⢰⠀
⠘⢷⣀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡴⢃⡴⠋⠀⠀⣰⢉⠇
⠀⠀⠉⣳⠦⢤⣤⣤⣤⠤⣮⠶⢻⡏⡀⢤⣲⠝⠚⠁⠀
⠀⠀⣰⠃⢠⠴⣚⡭⠖⠉⠀⠀⢸⡧⠚⠉⠀⠀⠀⠀⠀
⠀⢠⡏⠀⠐⠋⠁⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀
⠰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃ 
"""
    )

    parser = argparse.ArgumentParser(
        description="PdOS generates credentials and automates the login process for the intent of disrupting scam sites. A wordlist of names is required. I am not responsible for the misuse of this program. Report scam sites to https://safebrowsing.google.com/safebrowsing/report_phish/"
    )
    parser.add_argument(
        "-u", type=str, metavar="<url>", required=True, help="scam site url "
    )
    parser.add_argument(
        "-w",
        type=str,
        metavar="<path>",
        required=True,
        help="file path of names wordlist",
    )
    parser.add_argument(
        "-T", type=int, metavar="<threads>", default=1, help="number of threads to run"
    )
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    threads = []
    for _ in range(args.T):
        t = threading.Thread(target=pdos, args=(args.u, args.w))
        t.daemon = True
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(">> Keyboard Interrupt")
        sys.exit(130)
