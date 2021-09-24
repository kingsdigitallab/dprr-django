import regex


def parse_primary_source(text):
    """given a primary source text reference it returns the
    abbrev of the primary source
    """

    psource = ""

    ref_regex = regex.compile(
        r"""
                (?P<psource>(\w+\.?\s?)+)
                (\(?\d\)\s?)+
                """,
        regex.VERBOSE,
    )

    res = regex.search(ref_regex, text)

    if res:
        if res.group(psource):
            return res.group(psource)
        else:
            return None
    else:
        return None
