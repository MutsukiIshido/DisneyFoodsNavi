document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScriptが読み込まれました');

    const dropdownToggle = document.querySelector(".dropdown-toggle");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    if (!dropdownToggle || !dropdownMenu) return; // 要素がない場合はスクリプトを終了

    // **ページロード時にドロップダウンを非表示にする**
    dropdownMenu.style.display = "none";

    // 🔹 クリックイベントで開閉
    dropdownToggle.addEventListener("click", function (event) {
        event.preventDefault(); // リンクのデフォルト動作を防ぐ

        // **現在の表示状態をトグルする**
        if (dropdownMenu.style.display === "none" || dropdownMenu.style.display === "") {
            dropdownMenu.style.display = "block"; // 表示
        } else {
            dropdownMenu.style.display = "none"; // 非表示
        }
    });

    // 🔹 メニューの外をクリックしたら閉じる
    document.addEventListener("click", function (event) {
        if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = "none";
        }
    });

    // 🔹 フォームのリセットチェック
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("reset", () => {
            console.log("🚨 フォームがリセットされました！ 🚨");
        });
    }

    // 🔹 商品検索ボタン処理
    const openFoodSearchButton = document.getElementById('openFoodSearch');
    if (openFoodSearchButton) {
        openFoodSearchButton.addEventListener('click', function(event) {
            event.preventDefault();
            console.log('商品検索ボタンがクリックされました');

            // モーダルを表示
            const modal = new bootstrap.Modal(document.getElementById('foodModal'));
            modal.show();
        })
    }

    // 🔹 検索機能の処理
    const foodSearchInput = document.getElementById('foodSearch');
    const foodResults = document.getElementById('foodResults');
    const foodField = document.getElementById('id_food');

    if (foodSearchInput) {
        foodSearchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query) {
                fetch(`/food-search/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        foodResults.innerHTML = '';
                        data.forEach(food => {
                            const li = document.createElement('li');
                            li.className = 'list-group-item list-group-item-action';
                            li.textContent = food.name;
                            foodResults.appendChild(li);
                            li.onclick = () => {
                                console.log("✅ クリックされた商品:", food.name);

                                const foodField = document.getElementById('id_food');
                                const foodDisplay = document.getElementById('food_display');

                                if (!foodField || !foodDisplay) {
                                    console.error("🚨 必要な要素が見つかりません！");
                                    return;
                                }

                                // 商品名をセット
                                foodField.value = food.id;
                                foodDisplay.value = food.name;

                                foodField.dispatchEvent(new Event('change', { bubbles: true }));

                                // モーダルを閉じる
                                const modal = bootstrap.Modal.getInstance(document.getElementById('foodModal'));
                                modal.hide();
                            };
                        });
                    });
            } else {
                foodResults.innerHTML = '';
            }
        });
    }
});
