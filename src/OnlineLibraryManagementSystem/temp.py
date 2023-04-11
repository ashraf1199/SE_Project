import requests, webbrowser
from bs4 import BeautifulSoup

book_name = input("Book Name: ")
book_author = input("Book Author: ")
res1 = "Education"
google_link = 0
final_elements_list = -1

google_search = requests.get("https://www.google.com/search?tbm=bks&q=" + book_name + book_author)

soup = BeautifulSoup(google_search.text, 'html.parser')
search_results = soup.select('.kCrYT a')

for link in search_results[:1]:
    google_link = link.get('href')
    #webbrowser.open(google_link)

if google_link != 0:
    second_search = requests.get(google_link)
    soup1 = BeautifulSoup(second_search.text, 'html.parser')

    forId = soup1.find('link', rel="canonical")
    # print(forId)
    import re

    allStrings = re.findall(r'"(.*?)"', str(forId))
    print(allStrings[0])
    webbrowser.open(allStrings[0])
    final_link = requests.get(allStrings[0])
    soup2 = BeautifulSoup(final_link.text, 'html.parser')

    table_result = soup2.find('table', id="metadata_content_table")

    if table_result:
        rows = table_result.find_all('tr')
        fullstring = ""
        elements = ""

        for row in rows:

            if row.find('td', class_="metadata_label"):
                columns = row.find('td', class_="metadata_label").text
                # print(columns)
                fullstring += columns
                # print(fullstring)
            if fullstring.find("Subjects") != -1:
                if columns.find("Subjects") != -1:
                    list = row.find_all('span', itemprop="title")
                    # print(list)
                    for x in list:
                        sub_element = x.text
                        # print(sub_element)
                        elements = elements + sub_element + ">"
                    final_elements_list = elements.rstrip(">")
                    break
        #print("Education")
        res1 = "Education"
    else:
        # print("Education")
        res1 = "Education"
else:
    res1 = "Education"

if final_elements_list != -1:
    # print(res1 + ">" + final_elements_list)
    # res = res1 + ">" + final_elements_list
    if final_elements_list.endswith(">General"):
        res = final_elements_list[:-(len(">General"))]
    else:
        res = final_elements_list
    print(res)
else:
    res = res1
    print(res)
