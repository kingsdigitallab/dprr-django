# -*- coding: utf-8 -*-

import csv
from os import path

from promrep.models import (
    Province, PostAssertion, PostAssertionProvince
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
            print post_id

            try:
                pa = PostAssertion.objects.get(id=post_id)

                # TODO: only used if necessary to correct info
                # office_abbrev = row_dict.get("office_abbrev", "").strip()

                # provinces are separated by commas,
                # question mark indicates uncertainty
                province_str = row_dict.get("province", "")
                province_str = province_str.strip('"').strip("'")

                province_arr = [p.strip() for p in province_str.split(",")]
                print province_arr

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

                        # if created:
                        #     print("Created new province {}".format(province))

                        pap, created = \
                            PostAssertionProvince.objects.get_or_create(
                                post_assertion=pa,
                                province=province,
                                uncertain=unc
                            )
                    except:
                        print "missing_province: {}".format(prov)

            except:
                print "missing_postassertion: {}".format(post_id)


def run():
    ifname = "promrep/scripts/data/ProvincesV2.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
