from iatisum import *
import pandas as pd
import os
import shutil
from lxml import etree

if __name__ == '__main__':
    # Initialize flattener class
    iatiflat = IatiFlat()

    # Clean-up of old data; Make sure nothing important is in whatever folder you put here because it will be irrevocably erased
    shutil.rmtree("/home/alex/git/iati-sum/sep/")
    os.mkdir("/home/alex/git/iati-sum/sep/")

    # Where to look for saved IATI XML via registry-refresher
    rootdir = '/home/alex/git/IATI-Registry-Refresher/data'

    # Predefined header names
    header = iatiflat.header
    # Write a CSV that just consists of the full header. This will be cat'ed to the top of our concatinated total CSV after all donor CSVs have been written
    full_header = header + ["publisher_id"]
    header_frame = pd.DataFrame([full_header])
    header_frame.to_csv("/home/alex/git/iati-sum/sep/000header.csv", index=False, header=False, encoding="utf-8")

    partner_pubs = [
        "af",
        "afdb",
        "afd",
        "aics",
        "asdb",
        "ausgov",
        "enabel",
        "be-dgd",
        "bmgf",
        "gac-amc",
        "idrccrdi",
        "finance_canada",
        "caribank",
        "cif",
        "danida",
        "ebrd",
        "ec-devco",
        "ec-echo",
        "ec-near",
        "ec-fpi",
        "eib",
        "finland_mfa",
        "fao",
        "france",
        "bmz",
        "theglobalfund",
        "gpe",
        "iadb",
        "idlo",
        "ifcwbg",
        "ifad",
        "idea",
        "ilo",
        "imf",
        "iom",
        "irishaid",
        "jica",
        "lithuania_mfa",
        "millenniumchallenge",
        "mofa-jpn",
        "slovakaid",
        "minbuza_nl",
        "rvo",
        "mfat",
        "norad",
        "ofid",
        "odakorea",
        "uasd",
        "maec",
        "sida",
        "sdc_ch",
        "beis",
        "defra_transparency",
        "dfid",
        "dwp",
        "deccadmin",
        "dhsc",
        "fco",
        "hooda",
        "mrc",
        "ukmod",
        "scottish_government",
        "wfa",
        "unw",
        "unhabitat",
        "utd",
        "uncdf",
        "cerf",
        "unicef",
        "undp",
        "unesco",
        "un-environment",
        "unhcr",
        "unido",
        "unaids",
        "unops",
        "unocha",
        "unfpa",
        "wfp",
        "unitedstates",
        "usaid",
        "worldbank",
        "who",
        "unocha-cbpf"
    ]

    # Loop through all the folders downloaded via IATI registry refresh, and pass XML roots to our flatten_activities function.
    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            publisher = os.path.basename(subdir)
            if publisher in partner_pubs:
                print(filename)
                try:
                    root = etree.parse(filepath).getroot()
                except etree.XMLSyntaxError:
                    continue
                output = iatiflat.flatten_activities(root)
                if len(output) > 0:
                    data = pd.DataFrame(output)
                    data.columns = header
                    data['publisher_id'] = publisher
                    data.to_csv("/home/alex/git/iati-sum/sep/{}.csv".format(filename), index=False, header=False, encoding="utf-8")

    # Once individual (headless) CSVs are written for each donor. It's an easy step to concatenate them into one large document.
    # You may want to consider doing this in code rather than saving each donor's CSVs to disk, but I found this useful for
    # saving progress physically in case the conversion process gets interrupted
    os.system("cat /home/alex/git/iati-sum/sep/*.csv > /home/alex/git/iati-sum/iati.csv")
