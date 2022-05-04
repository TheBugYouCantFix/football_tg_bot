def handle_ambiguous_country_names(country: str) -> str:
    """
    Some countries are being called differently sometimes.
    This function gets the name of a country and returns the proper name for a csv file
    in case a country can be call in a few different ways

    :param country:
    :return:
    """
    country = country.lower().strip()

    if country == 'us' or country == 'usa' or country == 'united states of america':
        return 'united states'

    if country == 'uae':
        return 'United Arab Emirates'

    if country == 'russian federation':
        return 'russia'

    if country == 'czechia':
        return 'czech republic'

    if country == 'bih' or country == 'bosnia':
        return 'Bosnia and Herzegovina'

    return country
