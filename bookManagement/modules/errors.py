from django.shortcuts import render


def generic_error(request, exception):
    """Raising when unknown error occures."""
    template = 'error.html'
    error = """Something went wrong.
            If error occurs often please send error
            message contained below to administator."""
    error_message = str(exception)
    return render(request, template, {'em': error_message,
                                      'e': error})


def isbn_validation_error(request, template, form):
    """Raising when ISBN validation fails."""
    error = "Wrong ISBN ID!"
    return render(request, template, {'e': error,
                                      'form': form})


def date_error(request, template):
    """Raising when data validation fails."""
    error = "There is something wrong with date you have passed."
    return render(request, template, {'error': error})
