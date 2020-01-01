# The Shmoop Corpus

## Overview

This repository contains instructions for obtaining the *Shmoop corpus*. [Here](http://www.cs.toronto.edu/~makarand/shmoop/) is some more information about our project.

## Citation
<strong>The Shmoop Corpus: A Dataset of Stories with Loosely Aligned Summaries</strong>  
A. Chaudhury, M. Tapaswi, S. W. Kim, and S. Fidler  
arXiv: 1912.13082  
[Project page](http://www.cs.toronto.edu/~makarand/shmoop/) |
[arXiv](https://arxiv.org/abs/1912.13082)


## Download Instructions

1. Clone this repository.
2. Download and extract the contents of [stories.zip](http://www.cs.toronto.edu/~atef/stories.zip) and [manual_alignments.zip](http://www.cs.toronto.edu/~atef/manual_alignments.zip).
3. Contact support@shmoop.com to request permission to use Shmoop summaries for research purposes.
4. Run get_summaries.py to download the summaries from Shmoop.

## Contents

The two directories `summaries` and `stories` contain the summaries and stories respectively split by paragraph.

The `manual_alignments` directory contains the alignment information between summary and story paragraphs for the validation set.
Each row in the alignment files indicates to which paragraphs the given summary paragraph is aligned.
For example, `S2: 3, 6, 7` means an alignment between summary paragraph 2 and story paragraphs 3, 6, 7 (paragraphs are 0-indexed).

Other files include `get_summaries.py` which provides a simple script to download the summaries from Shmoop, `list_of_works.txt` which indicates the works which are included as well as those with manual annotations, and `sectioned_works.csv` which contains URLs used for download.

## Dependencies

- python3.x
- bs4 (for parsing HTML pages)
- nltk (for tokenization)
- tqdm (for download status)


## Example

An excerpt from Shakespeare's _A Midsummer Night's Dream_:

**Summary**

**S3:** Quince announces that Bottom is the paramour of a sweet voice, and Flute points out that he means "paragon."

**Original Text**

**D7:** QUINCE  Yea, and the best person too, and he is a very paramour for a sweet voice.

**D8:** FLUTE You must say “paragon.” A “paramour” is (God bless us) a thing of naught.

**Summary**

**S4:** Snug enters the house, announcing that the Duke is coming from the temple with two or three more couples who were just married.  Flute laments that, had they been able to perform, they'd no doubt be rich men, earning them at least sixpence a day (a royal pension).

**Original Text**

**D9:** _Enter Snug the joiner._

**D10:** SNUG Masters, the Duke is coming from the temple,	 and there is two or three lords and ladies more married. If our sport had gone forward, we had all been made men.

**D11:** FLUTE O, sweet bully Bottom! Thus hath he lost sixpence a day during his life. He could not have ’scaped sixpence a day. An the Duke had not given him sixpence a day for playing Pyramus, I’ll be hanged. He would have deserved it. Sixpence a day in Pyramus, or nothing!
