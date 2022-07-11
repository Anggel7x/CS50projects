import os
import random
import re
import sys
from numpy.random import choice

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
    # Keep track
    distribution = dict()
    # Search through all the htmls to see if they are linked in the PAGE
    n = 0
    for html in corpus:
        # Skips the actual page
        if html == page:
            continue
        elif html in corpus[page]:
            n += 1
    
    # Basic probabilities
    base_prob = (1-damping_factor)/len(corpus)
    if n != 0:
        presence_prob = damping_factor/n
    # Append the first element
    for html in corpus:
        if html in corpus[page] and n!= 0:
            distribution[html] = base_prob + presence_prob
        else :
            distribution[html] = base_prob
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Weights list
    def weights_list(corpus, current_page):
        weights = []
        transition = transition_model(corpus, current_page, DAMPING)
        for html in transition:
            weights.append(transition[html])
        return weights

    # Population List
    def population():
        popu = []
        for key in corpus:
            popu.append(key)
        return popu

    # Starting page
    current_page = random.sample(corpus.keys(),1)[0]

    # Looping
    page_ranks = dict()
    samples = list()
    for i in range(n):
        # Create a weighted list
        
        weights = weights_list(corpus, current_page)
        popu =  population()
        #Add sample
        sample = random.choices(population=popu, weights=weights, k=1)[0]
        samples.append(sample)
        # Now we are on the sampled webpage
        current_page = sample

    # Count every sample 
    for sample in samples:
        page_ranks[sample] = page_ranks.get(sample, 1) + 1

    # Assign Probability
    for page in page_ranks:
        page_ranks[page] = page_ranks[page]/SAMPLES

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Keep track of previous and news PageRanks
    new = dict()
    prev = dict()
    
    # Number of pages in the corpus
    N = len(corpus)
    # Starting point
    for key in corpus:
        prev[key] = 1.0/N
        new[key] = None
        
    # Base PageRank
    base_pr = (1.0-damping_factor)/N
    
    while True:
        # Relatives PageRank
        relatives_pr = dict()
        for html in corpus:
            for page in corpus:
                if html in corpus[page]:
                    relatives_pr[html] = relatives_pr.get(html,0) + prev[page]/len(corpus[page])
                else: 
                    relatives_pr[html] = relatives_pr.get(html,0)
            new[html] = base_pr + (damping_factor*relatives_pr[html])

        # Base case
        count = 0
        for html in corpus:
            if not abs(prev[html]-new[html]) <= 0.001:
                break
            count += 1
        if count == N:
            return new
        
        # Prev takes the new value
        for html in new:
            prev[html] = new[html]
                


if __name__ == "__main__":
    main()
