def breadcrumbs_context(request):
    breadcrumbs = []

    # 1. 最初に「ホーム」を追加
    breadcrumbs.append({"name": "ホーム", "url": "/home/"})

    # 2. 現在のページとリファラー（直前のページ）を取得
    current_path = request.path
    referer = request.META.get('HTTP_REFERER', '')

    # 3. 今いるページによって分岐

    # -------------------------
    # ① 直接表示するパターン
    # -------------------------
    simple_pages = {
        "/map/": "マップ（検索結果）",
        "/writereview/": "レビュー投稿",
        "/ranking/": "ランキング",
        "/favorite/": "お気に入り",
        "/readingreview/": "レビュー一覧",
        "/myreview/": "マイレビュー一覧",
        "/email_change/": "メールアドレス変更",
        "/password_change/": "パスワード変更"
    }

    if current_path in simple_pages:
        breadcrumbs.append({"name": simple_pages[current_path], "url": current_path})

    # -------------------------
    # ② 前のページを追うパターン（商品詳細・レビュー詳細）
    # -------------------------
    elif current_path.startswith("/food/"):  # 商品詳細
        # どこから来たかによってパンくずを追加
        if "map" in referer:
            breadcrumbs.append({"name": "マップ（検索結果）", "url": "/map/"})
        elif "ranking" in referer:
            breadcrumbs.append({"name": "ランキング", "url": "/ranking/"})
        elif "favorite" in referer:
            breadcrumbs.append({"name": "お気に入り", "url": "/favorite/"})
        elif "readingreview" in referer:
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})
        elif "myreview" in referer:
            breadcrumbs.append({"name": "マイレビュー一覧", "url": "/myreview/"})

        # 最後に「商品詳細」を追加（リンクは今のページ）
        breadcrumbs.append({"name": "商品詳細", "url": current_path})

    elif current_path.startswith("/review/"):  # レビュー詳細
        if "readingreview" in referer:
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})
        elif "myreview" in referer:
            breadcrumbs.append({"name": "マイレビュー一覧", "url": "/myreview/"})

        breadcrumbs.append({"name": "レビュー詳細", "url": current_path})

    return {"breadcrumbs": breadcrumbs}
