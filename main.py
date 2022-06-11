import pandas as pd
import numpy as np
import pycountry_convert as pc
import pycountry
import re

pub = pd.read_csv("data/tg/full.csv")
'Publication Type,Authors,Book Authors,Book Editors,Book Group Authors,Author Full Names,Book Author Full Names,Group Authors,Article Title,Source Title,Book Series Title,Book Series Subtitle,Language,Document Type,Conference Title,Conference Date,Conference Location,Conference Sponsor,Conference Host,Author Keywords,Keywords Plus,Abstract,Addresses,Affiliations,Reprint Addresses,Email Addresses,Researcher Ids,ORCIDs,Funding Orgs,Funding Name Preferred,Funding Text,Cited References,Cited Reference Count,"Times Cited, WoS Core","Times Cited, All Databases",180 Day Usage Count,Since 2013 Usage Count,Publisher,Publisher City,Publisher Address,ISSN,eISSN,ISBN,Journal Abbreviation,Journal ISO Abbreviation,Publication Date,Publication Year,Volume,Issue,Part Number,Supplement,Special Issue,Meeting Abstract,Start Page,End Page,Article Number,DOI,DOI Link,Book DOI,Early Access Date,Number of Pages,WoS Categories,Web of Science Index,Research Areas,IDS Number,Pubmed Id,Open Access Designations,Highly Cited Status,Hot Paper Status,Date of Export,UT (Unique WOS ID)'

print("Size of the dataset: {}".format(pub.shape))

# get yearly distribution
y = pub.groupby('Publication Year', as_index=False).count()[["Publication Year", "Publication Type"]]
print(y)
y.to_csv("data/tg/export/yearly_distribution.csv", index=False)

# get journals distribution
j = pub.groupby('Journal Abbreviation', as_index=False).count()[["Journal Abbreviation", "Publication Type"]]
print(j)
j.to_csv("data/tg/export/journals_distribution.csv", index=False)

# get types distribution
t = pub.groupby('Publication Type', as_index=False).count()[["Publication Type", "Authors"]]
print(t)
t.to_csv("data/tg/export/types_distribution.csv", index=False)

# get languages distribution
l = pub.groupby('Language', as_index=False).count()[["Language", "Publication Type"]]
print(l)
l.to_csv("data/tg/export/languages_distribution.csv", index=False)

# get average citations per year
c = pub.groupby('Publication Year', as_index=False).mean()[["Publication Year", "Times Cited, All Databases"]]
print(c)
c.to_csv("data/tg/export/citations_distribution.csv", index=False)


# get oa status distribution
oa = pub.groupby("Open Access Designations", as_index=False).count()[["Open Access Designations", "Publication Type"]]
oa.to_csv("data/tg/export/oa_distribution.csv", index=False)

# get universities (cities) of co-authors
cities = []
countries = []
for index, row in pub.iterrows():
    if pd.isna(row["Addresses"]):
        pass
    elif row["Author Full Names"].split(";") == 1:
        ad = re.sub('\[.*?\]', '', row["Addresses"])
        ct = ad.split(",")[-1].replace(";", "").strip().upper()
        if "USA" in ct.split(): ct = "USA"
        if "NY" in ct.split():  ct = "USA"
        if "AL" in ct.split():  ct = "USA"
        if "MD" in ct.split():  ct = "USA"
        if "OH" in ct.split():  ct = "USA"
        if "PA" in ct.split():  ct = "USA"
        if "VA" in ct.split():  ct = "USA"
        if "IL" in ct.split():  ct = "USA"
        if "KS" in ct.split():  ct = "USA"
        if "WI" in ct.split():  ct = "USA"
        if "DC" in ct.split():  ct = "USA"
        if "GA" in ct.split():  ct = "USA"
        if "ID" in ct.split():  ct = "USA"
        if "MA" in ct.split():  ct = "USA"
        if ct == "TOGO":
            c = ad.split(",")[-2].strip().upper()
            if "LOME" in c.split(): c = "LOME"
            if "KARA" in c.split(): c = "KARA"

            exists = False
            for ac in cities:
                if ac["city"] == c:
                    ac["count"] += 1
                    exists = True
            if not exists:
                cities.append({"city": c, "count": 1})

        exists = False
        for act in countries:
            if act["country"] == ct:
                act["count"] += 1
                exists = True
        if not exists:
            countries.append({"country": ct, "count": 1})
    else:
        a = re.sub('\[.*?\]', '', row["Addresses"])
        for ad in a.split(";"):
            ct = ad.split(",")[-1].replace(";", "").strip().upper()
            if "USA" in ct.split(): ct = "USA"
            if "NY" in ct.split():  ct = "USA"
            if "AL" in ct.split():  ct = "USA"
            if "MD" in ct.split():  ct = "USA"
            if "OH" in ct.split():  ct = "USA"
            if "PA" in ct.split():  ct = "USA"
            if "VA" in ct.split():  ct = "USA"
            if "IL" in ct.split():  ct = "USA"
            if "KS" in ct.split():  ct = "USA"
            if "WI" in ct.split():  ct = "USA"
            if "DC" in ct.split():  ct = "USA"
            if "GA" in ct.split():  ct = "USA"
            if "ID" in ct.split():  ct = "USA"
            if "MA" in ct.split():  ct = "USA"
            if ct == "TOGO":
                c = ad.split(",")[-2].strip().upper()
                if "LOME" in c.split(): c = "LOME"
                if "KARA" in c.split(): c = "KARA"

                exists = False
                for ac in cities:
                    if ac["city"] == c:
                        ac["count"] += 1
                        exists = True
                if not exists:
                    cities.append({"city": c, "count": 1})
            exists = False
            for act in countries:
                if act["country"] == ct:
                    act["count"] += 1
                    exists = True
            if not exists:
                countries.append({"country": ct, "count": 1})

ct = pd.DataFrame(cities)
ct.to_csv("data/tg/export/auth-cities_distribution.csv", index=False)

cto = pd.DataFrame(countries)
cto.to_csv("data/tg/export/auth-countries_distribution.csv", index=False)

continents = []
for ct in countries:
    try:
        c = ct["country"].upper()
        if c == "SENEGAMBIA" or c == "CENT AFR REPUBL" or c == "EQUAT GUINEA" or c == "SAO TOME & PRIN":
            continent = "AF"
        elif c == "BOSNIA & HERCEG":
            continent = "EU"
        elif c == "TIMOR-LESTE":
            continent = "AS"
        else:
            if "ENGLAND" in c:  c = "United Kingdom"
            if "SCOTLAND" in c:  c = "United Kingdom"
            if "NORTH IRELAND" in c:  c = "United Kingdom"
            if "COTE IVOIRE" in c:  c = "COTE D'IVOIRE"
            if "REP CONGO" in c:  c = "CONGO"
            if "PEOPLES R CHINA" in c:  c = "CHINA"
            if c == "LAOS":  c = "LAO"
            if "FED REP GER" in c:  c = "GERMANY"
            if "TRINIDAD TOBAGO" in c:  c = "TRINIDAD"
            if "UPPER VOLTA" in c:  c = "burkina faso"
            if "SWAZILAND" in c: c = "eswatini"
            if "U ARAB EMIRATES" in c: c = "UNITED ARAB EMIRATES"
            if "PAPUA N GUINEA" in c: c = "Papua New Guinea"
            if "GUINEA BISSAU" in c: c = "Guinea-Bissau"
            if "CAPE VERDE" in c: c = "Cabo Verde"
            c = pycountry.countries.search_fuzzy(c)[0].alpha_2
            continent = pc.country_alpha2_to_continent_code(c)
        exists = False

        for cto in continents:
            if cto["continent"] == continent:
                cto["count"] += ct["count"]
                exists = True
        if not exists:
            continents.append({"continent": continent, "count": ct["count"]})
    except:
        print(ct)

cto = pd.DataFrame(continents)
cto.to_csv("data/tg/export/auth-continents_distribution.csv", index=False)

print("ok")
# get journals countries/continents distribution
countries = []
continents = []
for index, row in pub.iterrows():
    try:
        a = row["Publisher Address"].split()[-1].strip()

        # custom filters
        if a == "ENGLAND": a = "United Kingdom"
        if "NY" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "AL" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "MD" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "PA" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "VA" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "IL" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "KS" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "WI" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "DC" in row["Publisher Address"].split(",")[-1].split():  a = "USA"
        if "ENGLAND" in row["Publisher Address"].split(",")[-1]:  a = "United Kingdom"
        if "SCOTLAND" in row["Publisher Address"].split(",")[-1]:  a = "United Kingdom"
        if row["Publisher Address"] == "MONTROUGE": a = "France"

        a = pycountry.countries.search_fuzzy(a)[0].alpha_2
        continent = pc.country_alpha2_to_continent_code(a)

        exists = False
        for ct in countries:
            if ct["country"] == a:
                ct["count"] += 1
                exists = True
        if not exists:
            countries.append({"country": a, "count": 1})

        exists = False
        for cto in continents:
            if cto["continent"] == continent:
                cto["count"] += 1
                exists = True
        if not exists:
            continents.append({"continent": continent, "count": 1})
    except:
        print(row["Publisher Address"])

ct = pd.DataFrame(countries)
ct.to_csv("data/tg/export/countries_distribution.csv", index=False)

cto = pd.DataFrame(continents)
cto.to_csv("data/tg/export/continents_distribution.csv", index=False)

# get authors list (/count)
authors = []
for index, row in pub.iterrows():
    au = row["Author Full Names"].split(";")
    for a in au:
        a = a.strip()
        exists = False
        for author in authors:
            if author["name"] == a:
                author["count"] += 1
                exists = True
        if not exists:
            authors.append({"name": a, "count": 1})

au = pd.DataFrame(authors)
au.to_csv("data/tg/export/authors_distribution.csv", index=False)

# get categories distribution
categories = []
for index, row in pub.iterrows():
    try:
        au = row["Research Areas"].split(";")
        for a in au:
            a = a.strip()
            exists = False
            for cat in categories:
                if cat["cat"] == a:
                    cat["count"] += 1
                    exists = True
            if not exists:
                categories.append({"cat": a, "count": 1})
    except:
        print(row["Research Areas"])

cat = pd.DataFrame(categories)
cat.to_csv("data/tg/export/categories_distribution.csv", index=False)
