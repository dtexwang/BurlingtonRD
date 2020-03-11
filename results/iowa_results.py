# Gregory Hogue (@gfjhogue)
# Python 3
#
# Run this script as-is to generate iowa_results.csv from
# https://results.thecaucuses.org

import csv
import xml.etree.ElementTree as ET
import urllib.request as request


IOWA_URL = "https://results.thecaucuses.org"


if __name__ == '__main__':

    res = request.urlopen(IOWA_URL)

    htmlStr = res.read()

    root = ET.fromstring(htmlStr)

    jsxClass = root.findall(".//div[@id='__next']/div")[0].attrib['class']

    precinctTable = root.findall(".//div[@class='"+jsxClass+" precinct-table']")[0]

    head = precinctTable.findall("./ul[@class='thead']/")
    candidates = []
    for col in head:
        candidates.append(col.text)

    subhead = precinctTable.findall("./ul[@class='sub-head']/")
    voteTypes = []
    for col in subhead:
        voteTypes.append(col.text)

    assert len(candidates) == len(voteTypes)

    candidate = ""
    header = [None] * len(candidates)
    for i in range(len(candidates)):
        if candidates[i] is not None:
            candidate = candidates[i]
        if voteTypes[i] is None:
            header[i] = candidate
        else:
            header[i] = candidate + " " + voteTypes[i]

    countySections = precinctTable.findall("./div/div[@class='precinct-data']/..")

    with open('iowa_results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(header)

        for countySection in countySections:
            county = " ".join(countySection.attrib['class'].split()[1:-1])

            precinctRows = countySection.findall("./div[@class='precinct-data']/")
            for precinctRow in precinctRows:

                row = [county] + [li.text.replace(",","") for li in precinctRow]
                csvwriter.writerow(row)