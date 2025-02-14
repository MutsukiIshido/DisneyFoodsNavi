def breadcrumbs_context(request):
    breadcrumbs = []
    
    # ホームを最初に追加
    if not breadcrumbs or breadcrumbs[0]["name"] != "ホーム":
        breadcrumbs.append({"name": "ホーム", "url": "/home/"})

    # 現在のページを追加
    if request.path == "/map/":
        breadcrumbs.append({"name": "マップ（検索結果）", "url": request.path})
    elif request.path == "/writereview/":
        breadcrumbs.append({"name": "レビュー投稿", "url": request.path})
    elif request.path == "/readingreview/":
        breadcrumbs.append({"name": "レビュー閲覧", "url": request.path})
    elif request.path == "/myreview/":
        breadcrumbs.append({"name": "マイレビュー一覧", "url": request.path})
    elif request.path.startswith("/review/"):  # レビュー詳細ページ用
        referer = request.META.get('HTTP_REFERER', '')

        # 遷移元がマイレビューなら「マイレビュー一覧」を追加
        if "myreview" in referer:
            breadcrumbs.append({"name": "マイレビュー一覧", "url": "/myreview/"})
        elif "readingreview" in referer:
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})

        # 最後にレビュー詳細を追加
        breadcrumbs.append({"name": "レビュー詳細", "url": request.path})

    return {"breadcrumbs": breadcrumbs}
