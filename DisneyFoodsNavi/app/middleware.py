# app/middleware.py

class BreadcrumbsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 直前のURLを保存
        previous_path = request.session.get('previous_path')
        current_path = request.path

        if previous_path != current_path:
            request.session['previous_path'] = current_path

        response = self.get_response(request)
        return response
