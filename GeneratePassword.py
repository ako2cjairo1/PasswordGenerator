from sys import argv as param
from passwordmeter import test
from urllib.request import urlopen
from os.path import isfile
from random import choice, randint

# download the words.txt if we don't have it yet
if not isfile('words.txt'):
    print("Downloading words.txt ...")
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    with open('words.txt', 'wb') as s:
        s.write(urlopen(url).read())


def create_password(num_words=2, num_numbers=4, num_spcial=4, word_to_use=""):
    words_txt = open('words.txt', 'r').read().split("\n")
    special_chars = [" ", "!", "#", "$", "%", "&", "'",
                     "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "=", "?", "@", "[", "]", "^", "_", "{", "|", "}", "~"]
    pass_str = ""

    for _ in range(int(num_words)):
        if word_to_use:
            # use a specific keyword to use in password creation
            words_txt = [w for w in words_txt if word_to_use in w.lower()]

        pass_str += choice(words_txt).lower().capitalize()
        for _ in range(int(num_numbers) // int(num_words)):
            pass_str += str(randint(0, 9))
        for _ in range(int(num_spcial) // int(num_words)):
            pass_str += choice(special_chars)

    return pass_str


def create_strong_password():
    passowrd_count = 0
    print("\nGenerating strong password ...\n")

    while True:
        # use 2 english word found in Words.txt
        # use 4 numbers between 0 and 9
        # use 4 symbols using special character list
        password = create_password(num_words=2, num_numbers=4, num_spcial=4)
        strength = test(password)[0]
        passowrd_count += 1

        if strength >= acceptable_strength:
            print(
                f"Here's a password out of {passowrd_count} generated.")
            show_password(password, strength)
            exit()


def main():
    # password parameters from pipe
    _words_count = param[1] if len(param) > 1 else 0
    _numbers_count = param[2] if len(param) > 2 else 0
    _special_count = param[3] if len(param) > 3 else 0
    _word_to_use = param[4] if len(param) > 4 else ""

    password = create_password(num_words=_words_count, num_numbers=_numbers_count,
                               num_spcial=_special_count, word_to_use=_word_to_use)
    strength = test(password)[0]
    return (password, strength)


def show_password(_pass, _stren):
    print(f"Password: {_pass}")
    print(f"Strength: {'{:.0f}'.format(_stren * 100)}%\n")


if __name__ == "__main__":
    strength = 0.0
    acceptable_strength = 0.95
    password = ""

    if len(param) < 2:
        create_strong_password()
    else:
        # generate a one-time password
        (password, strength) = main()
        if password:
            show_password(password, strength)
            if strength < acceptable_strength:
                regen = input(
                    f"The ideal password strength is {'{:.0f}'.format(acceptable_strength * 100)}%.\nDo you want to generate a strong password? (y/n): ")

                if "y" in regen.lower():
                    create_strong_password()
                else:
                    exit()
