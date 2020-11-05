from django.core.paginator import(
    Paginator,
    EmptyPage,
    PageNotAnInteger
)


def paginator(objects, page, pageSize):
    """Paginates given QuerySet to table with given page size."""
    paginator = Paginator(objects, pageSize)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)
    return paginated
