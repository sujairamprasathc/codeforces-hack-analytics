import re
from operator import itemgetter
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

if (input('Configure Proxy [y / n] : ') == 'y'):
    from urllib.request import ProxyHandler
    from urllib.request import build_opener
    from urllib.request import install_opener
    from urllib.request import HTTPBasicAuthHandler
    from urllib.request import HTTPHandler
    proxy_ip_address = input('Proxy ip address : ')
    proxy_port = input('Proxy port : ')
    username = input('Username : ')
    password = input('Password : ')
    install_opener(build_opener(ProxyHandler({'http' : 'http://' + username + ':' + password + '@' + proxy_ip_address + ':' + proxy_port}), HTTPBasicAuthHandler(), HTTPHandler))


#Get the page and extract hack information
contest_id = input('Contest id number : ')
url = 'http://www.codeforces.com/contest/' + contest_id + '/hacks'

page_html = urlopen(url).read()
page_soup = soup(page_html, "html.parser")

hacks = page_soup.findAll("tr", {"class":""})
hacks = hacks[2:len(hacks)-1]

#Statistics
problem_hack_map = {}
hacker_hack_map = {}
hacker_detailed_hack_map = {}

for i in range(1,len(hacks)):
    hack_id = str(hacks[i].find("td", {"class" : "left"})).split()[2]
    [time_stamp, problem, test, verdict] = hacks[i].findAll("td", {"class" : "status-small"})
    time_stamp = str(time_stamp).split()[2] + ' ' + str(time_stamp).split()[3]
    problem_code = str(problem).split()[4]
    verdict = str(verdict)
    verddict = re.search('>(.*)</span>', verdict).group(1)

    if 'Invalid input' in verdict:
        continue
    elif 'Unsuccessful hacking attempt' in verdict:
        continue
    elif 'Successful hacking attempt' in verdict:
        if problem_hack_map.__contains__(problem_code):
            problem_hack_map[problem_code] += 1
        else:
            problem_hack_map[problem_code] = 1
    else:
        continue

    [hacker, defender] = hacks[i].findAll("a", {"class" : "rated-user"})
    hacker = re.search('>(.*)<', str(hacker)).group(1)
    if "legendary-user" in hacker:
        hacker = re.search('>(.*)<', hacker).group(1)+ re.search('</span>(.*)', hacker).group(1)
    defender = re.search('>(.*)<', str(defender)).group(1)

    if hacker_hack_map.__contains__(hacker):
        hacker_hack_map[hacker] += 1
        if hacker_detailed_hack_map[hacker].__contains__(problem_code):
            hacker_detailed_hack_map[hacker][problem_code] += 1
        else:
            hacker_detailed_hack_map[hacker] = {problem_code : 1}
    else:
        hacker_hack_map[hacker] = 1
        hacker_detailed_hack_map[hacker] = {problem_code : 1}


# Problems in descending order of hacks
print('\n\n')
for key, value in sorted(problem_hack_map.items(), key = itemgetter(1), reverse = True):
    print(key, value)
print('\n\n')

# Top 5 hackers
print('Top 5 hackers')
i = 0
for top_hacker_data in sorted(hacker_hack_map.items(), key = itemgetter(1), reverse = True):
    if (i == 5):
        break
    print(top_hacker_data)
    i += 1
