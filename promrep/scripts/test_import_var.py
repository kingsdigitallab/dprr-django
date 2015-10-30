# -*- coding: utf-8 -*-

import nose
import primary_source_aux as ps_aux


def test__parse_prim_source():
    res = ps_aux.parse_primary_source("Amm. Marc. XIV 6.8")

    print res
    assert res == "Amm. Marc. XIV"




