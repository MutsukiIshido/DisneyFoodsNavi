def breadcrumbs_context(request):
    breadcrumbs = []

    # 最初に「ホーム」は固定
    breadcrumbs.append({"name": "ホーム", "url": "/home/"})

    current_path = request.path
    origin = request.GET.get('origin')
    referer = request.META.get('HTTP_REFERER', '')

    if referer:
        referer = referer.split(request.get_host())[-1]  # ドメイン部分をカット

    # デバッグ用（確認用に必要なら残してもOK）
    # print(f"DEBUG: current_path={current_path}, origin={origin}, referer={referer}")

    # 商品詳細ページ（/food/〇〇）
    if current_path.startswith("/food/"):
        # originパラメータが存在すれば優先
        if origin is not None and origin.strip() != '':
            page_source = origin.strip().lower()
        else:
            # refererがあればパスから推測する
            if "favorite" in referer:
                page_source = "favorite"
            elif "map" in referer:
                page_source = "map"
            elif "ranking" in referer:
                page_source = "ranking"
            elif "readingreview" in referer:
                page_source = "readingreview"
            elif "myreview" in referer:
                page_source = "myreview"
            else:
                page_source = ""

        # パンくずリストを追加
        if page_source == "map":
            breadcrumbs.append({"name": "マップ（検索結果）", "url": "/map/"})
        elif page_source == "ranking":
            breadcrumbs.append({"name": "ランキング", "url": "/ranking/"})
        elif page_source == "favorite":
            breadcrumbs.append({"name": "お気に入り", "url": "/favorite/"})
        elif page_source == "readingreview":
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})
        elif page_source == "myreview":
            breadcrumbs.append({"name": "マイレビュー一覧", "url": "/myreview/"})
        elif page_source == "review_detail":
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})
            breadcrumbs.append({"name": "レビュー詳細", "url": ""})  

        breadcrumbs.append({"name": "商品詳細", "url": current_path})

    # レビュー詳細ページ（/review/〇〇）
    elif current_path.startswith("/review/"):
        if origin is not None and origin.strip() != '':
            page_source = origin.strip().lower()
        else:
            if "readingreview" in referer:
                page_source = "readingreview"
            elif "myreview" in referer:
                page_source = "myreview"
            else:
                page_source = ""

        if page_source == "readingreview":
            breadcrumbs.append({"name": "レビュー一覧", "url": "/readingreview/"})
        elif page_source == "myreview":
            breadcrumbs.append({"name": "マイレビュー一覧", "url": "/myreview/"})

        breadcrumbs.append({"name": "レビュー詳細", "url": current_path})

    # それ以外（単純なページ）
    else:
        simple_pages = {
            "/map/": "マップ（検索結果）",
            "/writereview/": "レビュー投稿",
            "/ranking/": "ランキング",
            "/favorite/": "お気に入り",
            "/readingreview/": "レビュー一覧",
            "/myreview/": "マイレビュー一覧",
            "/email_change/": "メールアドレス変更",
            "/password_change/": "パスワード変更",
        }
        if current_path in simple_pages:
            breadcrumbs.append({"name": simple_pages[current_path], "url": current_path})

    return {"breadcrumbs": breadcrumbs}
