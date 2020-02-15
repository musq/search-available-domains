#!/usr/bin/env python3

# Script to find out available domains
# - using dictionary words
# - using dynamically generated pronounceable words

# Author: Ashish Ranjan (https://github.com/musq)
# License: GNU GPLv3, or later version

from nltk.corpus import words
from pronounceable import PronounceableWord, Pronounceablity
from time import sleep

import sys
import whois


AVAILABLE_DOMAINS_FILE = 'domains.txt'
WHOIS_REQUESTS_FILE = 'requests.txt'
EXCEPTIONS_FILE = 'exceptions.txt'

DOMAIN_MAX_LENGTH = 2
DOMAIN_MAX_SYLLABLE_COUNT = 2
MAX_DESIRED_RESULTS = 500
SLEEP_INTERVAL = 0.2

ALL_TLD = ['com', 'ro']


open(AVAILABLE_DOMAINS_FILE, 'a').close()
open(WHOIS_REQUESTS_FILE, 'a').close()


def find_dictionary_words():
    words_list = list(set(
        [ w.lower() for w in words.words() \
            if len(w) == DOMAIN_MAX_LENGTH ]
    ))
    words_list.sort()

    for word in words_list:
        for tld in ALL_TLD:
            domain = word + '.' + tld

            if log_whois_requests(domain) \
                and whois_availability(domain):

                print(domain)
                store_available_domain(domain)
                sleep(SLEEP_INTERVAL)


def find_pronounceable_words():
    pr = Pronounceablity()

    for x in range(0, MAX_DESIRED_RESULTS):
        while True:
            word = PronounceableWord().length(
                DOMAIN_MAX_LENGTH,
                DOMAIN_MAX_LENGTH+1
            )
            syllable_count = pr.syllable(word)

            if (syllable_count > DOMAIN_MAX_SYLLABLE_COUNT):
                continue

            any_available = False
            for tld in ALL_TLD:
                domain = word + '.' + tld

                if log_whois_requests(domain):
                    available = whois_availability(domain)

                    if available:
                        print(domain)
                        store_available_domain(domain)

                    any_available = any_available or available
                    sleep(SLEEP_INTERVAL)

            if any_available:
                break


def whois_availability(domain):
    try:
        detail = whois.whois(domain)

        if detail['registrar'] is None:
            return True

    except whois.parser.PywhoisError:
        return True

    except KeyboardInterrupt:
        raise

    except:
        e = sys.exc_info()[0]
        print(str(e), domain)

        with open(EXCEPTIONS_FILE, 'a') as f:
            f.write(domain + '\n')

    return False


def log_whois_requests(domain):
    with open(WHOIS_REQUESTS_FILE, 'r') as file:
        for row in file:
            if (domain == row.rstrip()):
                return False

    with open(WHOIS_REQUESTS_FILE, 'a') as file:
        file.write(domain + '\n')

    return True


def main():
    find_dictionary_words()
    # find_pronounceable_words()


def store_available_domain(domain):
    with open(AVAILABLE_DOMAINS_FILE, 'a') as file:
        file.write(domain + '\n')


if __name__ == "__main__":
    main()
