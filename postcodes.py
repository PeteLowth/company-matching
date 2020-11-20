import pandas as pd
import numpy as np

def clean_postcode(postcode):
    # Convert x to a pandas series
    postcode = pd.Series(np.atleast_1d(postcode))

    # Upper case, alphanumeric, no whitespace
    postcode = postcode.str.replace('[^\w]', '').str.upper()

    # Upper case, alphanumeric, no whitespace
    postcode = postcode.str.replace('[^\w]', '').str.upper()

    return postcode


def postcode_breakdown(postcode):
    """
    postcode: string or list/series of strings

    If a valid postcode is given, outputs a dataframe with the postcode area, district, sector and full postcode
    Otherwise, returns NaNs
    """

    postcode = clean_postcode(postcode)

    # UK postcode regex: [1 or 2 letters][1 or 2 letters/numbers][any number of spaces][1 number][2 letters]
    pattern = r'^([A-Z]{1,2})([0-9A-Z]{1,2})[\s]*([0-9])([A-Z]{2})'

    postcode_breakdown = postcode.str.extract(pattern)

    postcode_breakdown['postcode_area'] = postcode_breakdown[0]
    postcode_breakdown['postcode_district'] = postcode_breakdown['postcode_area'] + postcode_breakdown[1]
    postcode_breakdown['postcode_sector'] = postcode_breakdown['postcode_district'] + ' ' + postcode_breakdown[2]
    postcode_breakdown['postcode_full'] = postcode_breakdown['postcode_sector'] + postcode_breakdown[3]

    postcode_breakdown.drop(columns=[0, 1, 2, 3], inplace=True)

    return postcode_breakdown


def detect_postcode_type(postcode):
    """
    returns the type of postcode given (area, district, sector, full, none)
    """
    postcode_pattern = r'^[A-Z]{1,2}[0-9]{1}[0-9A-Z]{0,1}[\s]*[0-9][A-Z]{2}$'
    district_pattern = r'^[A-Z]{1,2}[0-9]{1}[0-9A-Z]{0,1}$'
    area_pattern = r'^[A-Z]{1,2}$'

    postcode = clean_postcode(postcode)

    # Convert x to a pandas series
    postcode = pd.Series(np.atleast_1d(postcode))

    postcode_type = np.where(
        postcode.str.match(postcode_pattern), 'postcode',
        np.where(
            postcode.str.match(district_pattern), 'district',
            np.where(
                postcode.str.match(area_pattern), 'area', 'none'
            )
        )
    )

    return postcode_type
