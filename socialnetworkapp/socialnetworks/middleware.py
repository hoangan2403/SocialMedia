from django.utils.deprecation import MiddlewareMixin


class OAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print("do")
        if request.path_info == '/auth/token/' and request.method == 'POST':
            request.POST = request.POST.copy()
            request.POST['client_id'] = 'pXqUHJut8GsjpO1lSJ9XRerB1RNrzvjJFCEOvbfA'
            request.POST['client_secret'] = 'u2r9PB2WfWv0rjOSarwlIEF4nfYsjkz29XuwmZ0j2phdxCm86ay4xmWLlxMRahYXcxx6oI6wI80e9aZyu1d2y39gwwnCFXCCcS4tgK6MRrDNxhjAQxY31cdGr36VQcnF'
            request.POST['grant_type'] = 'password'