def breadcrumbs_context(request):
    breadcrumbs = []
    
     # ホームを最初に追加（ただし、すでにある場合は追加しない）
    if not breadcrumbs or breadcrumbs[0]["name"] != "ホーム":
        breadcrumbs.append({"name": "ホーム", "url": "/"})

    # 現在のページを追加
    if request.path == "/map/":
        breadcrumbs.append({"name": "マップ（検索結果）", "url": request.path})
    elif request.path == "/writereview/":
        breadcrumbs.append({"name": "レビュー投稿", "url": request.path})
    elif request.path == "/readingreview/":
        breadcrumbs.append({"name": "レビュー閲覧", "url": request.path})
    elif request.path == "/myreview/":
        breadcrumbs.append({"name": "マイレビュー一覧", "url": request.path})
    elif request.path == "/review_detail/":
        breadcrumbs.append({"name": "レビュー詳細", "url": request.path})
    elif request.path == "/ranking/":
        breadcrumbs.append({"name": "ランキング", "url": request.path})
    elif request.path == "/favorite/":
        breadcrumbs.append({"name": "お気に入り一覧", "url": request.path})
    elif request.path == "/email_change/":
        breadcrumbs.append({"name": "メールアドレス変更", "url": request.path})
    elif request.path == "/password_change/":
        breadcrumbs.append({"name": "パスワード変更", "url": request.path})
    # 他のページの処理も追加
    
    # デバッグ用（サーバー起動後、ターミナルで確認）
    print("Breadcrumbs:", breadcrumbs)
    
    
    return {"breadcrumbs": breadcrumbs}
