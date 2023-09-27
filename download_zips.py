from multiprocessing import Pool
from pathlib import Path

import requests
import re


def get_meeting_links():
    raw_data = requests.get("https://jvet-experts.org/doc_end_user/all_meeting.php").text
    unprosessed = [x for x in raw_data.split("\r\n") if "href" in x]
    # Extract the link from
    # 		<td width="*" align="center"><a href="current_meeting.php?id_meeting=196&search_id_group=1&search_sub_group=1">Hannover</a></td>
    m = re.compile(r'\t\t<td width="\*" align="center"><a href="current_meeting\.php\?id_meeting=(\d+)&search_id_group=1&search_sub_group=1">(\w+\s?\w+)<\/a><\/td>')
    links = []
    for x in unprosessed:
        match = m.match(x)
        links.append((match.group(2), "https://jvet-experts.org/doc_end_user/current_meeting.php?id_meeting=" + match.group(1)))
    return links


def download_links_for_one_meeting(meeting_link):
    raw_data = requests.get(meeting_link).text
    unprosessed = [x for x in raw_data.split("\r\n") if "href" in x and "Download" in x and "javascript" not in x]
    dl_links = []
    m = re.compile(r'<a href="\.\.\/doc_end_user\/documents\/(.*)">(.*)&nbsp;')
    for x in unprosessed[:-1]:
        dl_links.append(("https://jvet-experts.org/doc_end_user/documents/" + m.search(x).group(1), m.search(x).group(2)))
    return dl_links


def download_one(link):
    r = requests.get(link[0])
    with open("contents/" + link[1], "wb") as f:
        f.write(r.content)
        print("Downloaded", link[1])


if __name__ == '__main__':
    links = get_meeting_links()
    dl_links = []
    for x in links:
        dl_links.extend(download_links_for_one_meeting(x[1]))
    Path("contents").mkdir(exist_ok=True)
    with Pool(10) as p:
        p.map(download_one, dl_links)
