from django.conf import settings
from django.core.exceptions import SuspiciousOperation


def QueryStringsSanitizer(get_response):

    def wrapper(request):

        path = request.path
        path_info = request.path_info

        for rm in settings.QUERY_REMOVE_STRINGS:
            path = path.replace(rm, '')
            path_info = path_info.replace(rm, '')

        if path != request.path or path_info != request.path_info:
            raise SuspiciousOperation('Invalid URL')

        if True:
            # Only apply to get requests
            query_strings = []

            for (key, value) in dict(request.GET.lists()).items():

                try:
                    # replace not allowed strings with '' for each querystring value.
                    for rm in settings.QUERY_REMOVE_STRINGS:
                        # Value is it list for example:
                        # ?name=test   with be received here in format: {'name': ['test']}
                        value[0] = value[0].replace(rm, '')
                except:
                    # Ignore if any error happened
                    # TODO: Check situations that lead to here, may cause some leaks!
                    continue

                # Now cleaned data push to final list
                query_strings.append((key, value[0]))

            edit_get = request.GET.copy()
            # Get a copy of request.GET and update filtered values to new ones.
            for i in range(len(query_strings)):
                edit_get[query_strings[i][0]] = query_strings[i][1]

            request.GET = edit_get

            # Only apply to get requests
            query_strings = []

            for (key, value) in dict(request.POST.lists()).items():

                try:
                    # replace not allowed strings with '' for each querystring value.
                    for rm in settings.QUERY_REMOVE_STRINGS:
                        # Value is it list for example:
                        # ?name=test   with be received here in format: {'name': ['test']}
                        value[0] = value[0].replace(rm, '')
                except:
                    # Ignore if any error happened
                    # TODO: Check situations that lead to here, may cause some leaks!
                    continue

                # Now cleaned data push to final list
                query_strings.append((key, value[0]))

            edit_get = request.POST.copy()
            # Get a copy of request.GET and update filtered values to new ones.
            for i in range(len(query_strings)):
                edit_get[query_strings[i][0]] = query_strings[i][1]

            request.POST = edit_get

            response = get_response(request)

        return response

    return wrapper
