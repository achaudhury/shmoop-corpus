from builtins import zip, str, range
import pdb, os, csv, re, io
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm
import common.util as util
from shutil import rmtree
from nltk.tokenize import word_tokenize, sent_tokenize

# PARAMS
SUMMARY_DIR = 'summaries'
MAIN_SITE = 'https://www.shmoop.com'

# Summary list info
summary_list_file = "data/metadata/sectioned_works.csv"

# Get contents of the summary file
summary_infos = util.get_csv_contents(summary_list_file)

# Omit these works as they need to be done manually
omitted_works = set(["Don Quixote", "Grimms' Fairy Tails", "Ulysses", "The Communist Manifesto", "The Hunchback of Notre-Dame", "Robinson Crusoe"])
summary_infos = [x for x in summary_infos if x[1] not in omitted_works]

## Function to limit summary bullets to 250 tokens, splitting by end of sentence otherwise
LIMIT = 250
def apply_para_size_limit(split, limit):

    if len(word_tokenize(split)) < limit:
        return [split]

    result = []
    sentences = sent_tokenize(split)

    current_split = str("")
    current_len = 0
    for s in sentences:
        sent_len = len(word_tokenize(s))
        if (current_len + sent_len) < limit:
            if not s[-1].isspace():
                s += str(" ")
            current_split += s
            current_len += sent_len
        else:
            result.append(current_split)
            current_split = s
            current_len = sent_len

    if current_len > 0:
        result.append(current_split)

    return result



# For each summary info
for _, title, url, _, _  in tqdm(summary_infos):

    # Create a directory for the work if needed
    specific_summary_dir = os.path.join(SUMMARY_DIR, title)
    if not os.path.exists(specific_summary_dir):
        os.makedirs(specific_summary_dir)

    # Parse work page
    soup = BeautifulSoup(urllib.request.urlopen(MAIN_SITE + str(url) + '/summary.html'), "html.parser")
    sections = soup.findAll("li", {"class" : "inner-list"})
    section_titles = [x.text for x in sections]
    section_urls = [x.a['href'] for x in sections]
    pdb.set_trace()

    # For each section
    for index, section_title, section_url in zip(list(range(len(section_titles))), section_titles, section_urls):

        # Get summary content
        soup = BeautifulSoup(urllib.request.urlopen(MAIN_SITE + url + '/' + section_url), "html.parser")
        lines = [l.text for l in soup.find_all("div", {"id": "div_PrimaryContent"})[0].findChildren("li")]

        sized_splits = []
        for l in lines:
            sized_splits.extend(apply_para_size_limit(l, LIMIT))

        # Save in a file
        with io.open(os.path.join(specific_summary_dir, str(index) + '.txt.utf8'), 'w', encoding="utf-8") as f:
            for split in sized_splits:
                if len(split) == 0 or split[-1] != "\n":
                    split = split + str("\n")
                f.write(split)
                f.write(str("\n"))


