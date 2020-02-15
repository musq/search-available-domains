# Search available domains

Find out available domains using whois.

It works by iterating over a list of words which fit the specified parameters and checking whois to see if entries already exist. If it does not exist, this domain is stored as an available.

### Requirements

- python 3.6+

### Installation

```bash
# Clone this repository and `cd` into it
git clone https://github.com/musq/search-available-domains
cd search-available-domains

# Create virtualenv
python -m venv .venv
source .venv/bin/activate

# Install dependencies
python -m pip install -U pip
python -m pip install -r requirements.txt

# Run the script
python main.py
```

### Issues

If you face issues with *nltk*, please get a shell of your virtualenv's python by typing `python` and then follow these ---

```
import nltk
nltk.download('words')
```

You'll need to do this only once.

### Configuration

There are two modes to choose candidates for potential usernames. Check the `main()` function in `main.py`.

1. **Dictionary** *(default)* --- Use words from a dictionary
1. **Pronounceable** --- Use random pronounceable words with a threshold on syllables. Use following parameters:
    - `DOMAIN_MAX_SYLLABLE_COUNT` - Maximum syllables count
    - `MAX_DESIRED_RESULTS` - Number of usernames to scout

Other generic parameters ---

- `DOMAIN_MAX_LENGTH` - Length of desired domain
- `SLEEP_INTERVAL` - Break after each whois ping. (Keep this greater than 200ms to avoid being blacklisted by whois servers)
- `AVAILABLE_DOMAINS_FILE` - File name to store the available usernames
- `WHOIS_REQUESTS_FILE` - File name to store all tried words
- `EXCEPTIONS_FILE` - File name to store all exceptions

### Optimizations

- Check if the current word has already been pinged. If yes, do not ping it again.
