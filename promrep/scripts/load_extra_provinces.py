# -*- coding: utf-8 -*-

import csv
from os import path

from promrep.models import (
    Province, PostAssertion, Office, PostAssertionProvince
)

ICSV_COLUMNS = ["post_id", "office_abbrev", "province"]


def read_input_file(ifname):  # noqa

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile, fieldnames=ICSV_COLUMNS,)

        # skips first row
        csvDict.next()

        for row_dict in csvDict:
            post_id = int(row_dict["post_id"])

            pa = None
            try:
                pa = PostAssertion.objects.get(id=post_id)
            except:
                print("PostAssertion not found {}".format(post_id))

            if pa:
                # only used if necessary to correct info
                office_abbrev = row_dict.get("office_abbrev", "").strip()

                if office_abbrev:
                    office_abbrev = office_abbrev.lower().strip(".").strip(",")
                    office_abbrev = office_abbrev + "."

                    office = Office.objects.get(
                        abbrev_name__iexact=office_abbrev)

                    pa.office = office
                    pa.save()
                    print("Updated office for PostAssertion {}".format(pa.id))

                # provinces are separated by commas,
                # question mark indicates uncertainty
                province_str = row_dict.get("province", "")
                province_str = province_str.strip('"').strip("'")

                province_arr = [p.strip() for p in province_str.split(",")]

                for prov in province_arr:
                    if "?" in prov:
                        prov = prov.strip("?")
                        unc = True
                    else:
                        unc = False

                    print row_dict

                    try:
                        province = Province.objects.get(
                            name__iexact=prov.lower()
                        )
                    except:
                        province = Province(name=prov)
                        province.save()

                        print("Created new province {}".format(province))

                    pap, created = \
                        PostAssertionProvince.objects.get_or_create(
                            post_assertion=pa,
                            province=province,
                            uncertain=unc
                        )


def run():
    ifname = "promrep/scripts/data/ProvincesV3.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
