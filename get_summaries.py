from builtins import zip, str, range
import pdb, os, csv, re, io
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm
from shutil import rmtree
from nltk.tokenize import word_tokenize, sent_tokenize

# PARAMS
SUMMARY_DIR = 'summaries'
MAIN_SITE = 'https://www.shmoop.com'

# Summary list info
summary_list_file = "sectioned_works.csv"

# Get contents of the summary file
with open(summary_list_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    summary_infos = list(reader)

# Omit these works as they need to be done manually
omitted_works = set(["Don Quixote", "Grimms' Fairy Tails", "Ulysses", "The Communist Manifesto", "The Hunchback of Notre-Dame", "Robinson Crusoe"])
summary_infos = [x for x in summary_infos if x[1] not in omitted_works]
print("Note the following works while used in the analysis, require additional manual parsing and are not included in the dataset:")
print(omitted_works)

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
error_files, error_titles = [], []
for k, (_, title, url, _, _) in enumerate(summary_infos):
    print('\n>>> {}. {} <<<'.format(k, title))

    # Create a directory for the work if needed
    specific_summary_dir = os.path.join(SUMMARY_DIR, title)
    if not os.path.exists(specific_summary_dir):
        os.makedirs(specific_summary_dir)

    # If complete, ignore and be done
    num_atefs_files = len(os.listdir(os.path.join('submission', specific_summary_dir)))
    num_new_files = len(os.listdir(specific_summary_dir))
    if num_atefs_files == num_new_files:
        print('Completed.')
        continue

    # Parse page
    html_address = MAIN_SITE + str(url) + '/summary.html'
    soup = BeautifulSoup(urllib.request.urlopen(html_address), "html.parser")
    sections = soup.findAll("li", {"data-class" : "SHEvent"})

    # Go over each section
    for index, section in enumerate(sections):
        output_fname = os.path.join(specific_summary_dir, str(index) + '.txt.utf8')
        if os.path.exists(output_fname):
            print('Found section: {}'.format(index))
            continue

        # Parse section to get bullet point text
        print('Parsing section: {}'.format(index))
        section_points = section.findAll("ul", {"id": ""})
        summary_bullets = []
        for group_points in section_points:
            summary_bullets += group_points.findAll("li")
        lines = [bullet.text for bullet in summary_bullets]

        # Fix weird newline issue
        for k in range(len(lines)):
            lines[k] = lines[k].replace('\n', '\n\n')

        # Split
        sized_splits = []
        for l in lines:
            sized_splits.extend(apply_para_size_limit(l, LIMIT))

        # Save in a file
        with io.open(output_fname, 'w', encoding="utf-8") as f:
            for split in sized_splits:
                if len(split) == 0 or split[-1] != "\n":
                    split = split + str("\n")
                f.write(split)
                f.write(str("\n"))
