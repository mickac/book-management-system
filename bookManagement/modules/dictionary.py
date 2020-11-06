def build_date_searchword(keyword, parameter):
    if len(keyword) == 2:
        return {(parameter + "__icontains"): keyword}
    elif len(keyword) == 1:
        return {(parameter + "__exact"): keyword}
    raise ValueError