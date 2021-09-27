from django.utils.deprecation import MiddlewareMixin


class SimpleMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.variable = 'edilson'

    def process_response(self, request, response):
        ref = request.GET.get('ref', None)
        return response
