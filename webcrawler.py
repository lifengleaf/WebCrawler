# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:07:41 2016

@author: Leaf
"""

# get the page content of a requested url
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ''


        
# get the first link on a page and the end position of the link               
def get_next_target(page):
    start_link = page.find('<a href=' )
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote+1 : end_quote]
    return url, end_quote



# extract all the links on a requested page        
def get_all_links(page): 
    links = [] 
    while True: 
        url, endpos = get_next_target(page)
        if url: 
            links.append(url)
            page = page[endpos:] 
        else: 
            break 
    return links



# add a keyword/url pair to index dictionary
def add_to_index(index, keyword, url): 
    # keyword in dictionary
    if keyword in index:
        index[keyword].append(url) 
    else:
        index[keyword] = [url]
        

        
# split page content into keywords, and add keyword/url pairs to index
def add_page_to_index(index, url, content): 
    words = content.split() 
    for word in words: 
        add_to_index(index, word, url) 

        
# help function to union two arrays
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
            
            
# crawl the web and get a index dictionary and graph dictionary
# graph maps all the links that link to one target page
def crawl_web(seed):     
    tocrawl = [seed] 
    crawled = [] 
    index = {} 
    graph = {}
    
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled: 
            content = get_page(page) 
            add_page_to_index(index, page, content) 
            outlinks= get_all_links(content)            
            graph[page] = outlinks
            union(tocrawl, outlinks) 
            crawled.append(page)             
    return index, graph
    


# compute rank of a page
def compute_ranks(graph):
    d = 0.8  # damping constant
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks



# search the url of a requested keyword
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return None
    


# get the url most likely to be the best site for a requested keyword
def lucky_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    return best_page



# use quick sort algorithm to order array
def quick_sort(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]]
        worse = []
        better = []
        for page in pages[1:]:
            if ranks[page] <= pivot:
                worse.append(page)
            else:
                better.append(page)
    return quick_sort(better, ranks) + [pages[0]] + quick_sort(worse, ranks)



# get a list of all urls for a keyword, ordered by page rank
def ordered_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    return quick_sort(pages, ranks)


index, graph = crawl_web('http://www.udacity.com/cs101x/urank/index.html');
ranks = compute_ranks(graph)
print lucky_search(index, ranks, 'Hummus')
print ordered_search(index, ranks, 'Hummus')



