def breadcrumbs_context(request):
    path = request.path.strip('/').split('/')
    breadcrumbs = []
    url = "/"

    for segment in path:
        url += segment + "/"
        breadcrumbs.append({"name": segment.capitalize(), "url": url})

    return {"breadcrumbs": breadcrumbs}
