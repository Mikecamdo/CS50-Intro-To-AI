import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = { }

    links = corpus[page]
    num_links = len(links)

    if num_links == 0: # if no outgoing links, randomly choose between all pages
        for a_page in corpus:
            probability_distribution[a_page] = 1 / len(corpus)
        return probability_distribution

    for link in links: # random surfer chooses link on page 
        probability_distribution[link] = (1 / num_links) * damping_factor

    random_probability = (1 - damping_factor) / len(corpus) # random surfer choose random page
    for a_page in corpus:
        if a_page in probability_distribution:
            probability_distribution[a_page] += random_probability
        else:
            probability_distribution[a_page] = random_probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = { }
    current_page = random.choice(list(corpus.keys()))
    page_rank[current_page] = 1

    for i in range(n - 1):
        probability_distribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(probability_distribution.keys()), list(probability_distribution.values()))[0]
        if current_page in page_rank:
            page_rank[current_page] += 1
        else:
            page_rank[current_page] = 1

    for page in corpus: # ensures every page in the corpus exists in the page_rank dictionary
        if page not in page_rank:
            page_rank[page] = 0

    for rank in page_rank: # calculates proportion of all samples that correspond to each page
        page_rank[rank] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = { }
    num_pages = len(corpus)

    for page in corpus: # start by giving each page a rank of 1 / num_pages
        page_rank[page] = 1 / num_pages

    
    while True:
        max_change_in_value = 0
        for rank in page_rank:
            second_condition = 0
            for page, links in corpus.items():
                if rank in links:
                    second_condition += (page_rank[page] / len(links))
                elif len(links) == 0:
                    second_condition += (page_rank[page] / len(corpus))

            old_value = page_rank[rank]
            page_rank[rank] = ((1 - damping_factor) / num_pages) + damping_factor * second_condition
            change_in_value = page_rank[rank] - old_value
            if abs(change_in_value) > max_change_in_value:
                max_change_in_value = abs(change_in_value)

        if max_change_in_value <= 0.001: # end function when values stop changing by more than 0.001
            return page_rank


if __name__ == "__main__":
    main()
