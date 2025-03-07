document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScriptが読み込まれました');

    // **🔹 ドロップダウンメニュー制御**
    const dropdownToggle = document.querySelector(".dropdown-toggle");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    if (!dropdownToggle || !dropdownMenu) return;

    dropdownMenu.style.display = "none";

    dropdownToggle.addEventListener("click", function (event) {
        event.preventDefault();
        dropdownMenu.style.display = (dropdownMenu.style.display === "none") ? "block" : "none";
    });

    document.addEventListener("click", function (event) {
        if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = "none";
        }
    });

    // **🔹 フォームのリセットチェック**
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("reset", () => {
            console.log("🚨 フォームがリセットされました！ 🚨");
        });
    }

    // **🔹 商品検索モーダル**
    const openFoodSearchButton = document.getElementById('openFoodSearch');
    if (openFoodSearchButton) {
        openFoodSearchButton.addEventListener('click', function(event) {
            event.preventDefault();
            const modal = new bootstrap.Modal(document.getElementById('foodModal'));
            modal.show();
        });
    }

    // 🔹 商品検索機能
    const foodSearchInput = document.getElementById('foodSearch');
    const foodResults = document.getElementById('foodResults');
    const foodField = document.getElementById('id_food');
    const foodDisplay = document.getElementById('food_display');

    if (foodSearchInput) {
        foodSearchInput.addEventListener("input", function () {
            const query = this.value.trim();
            console.log("🔍 検索ワード:", query);  // 🔍 デバッグ用
            
            if (query.length > 0) {
                fetch(`/food-search/?q=${query}`)
                    .then(response => {
                        console.log("✅ レスポンスステータス:", response.status);  // 🔍 デバッグ用
                        return response.json();
                    })
                    .then(data => {
                        console.log("📄 取得したデータ:", data);  // 🔍 デバッグ用
                        foodResults.innerHTML = "";
                        if (data.length === 0) {
                            foodResults.innerHTML = "<li class='list-group-item'>該当なし</li>";
                            return;
                        }
                        data.forEach(food => {
                            const li = document.createElement("li");
                            li.className = "list-group-item list-group-item-action";
                            li.textContent = food.name;
                            li.onclick = () => {
                                console.log("✅ 選択した商品:", food.name);
                                foodField.value = food.id;
                                foodDisplay.value = food.name;

                                // 🟢 **モーダルを適切に閉じる**
                                const foodModal = bootstrap.Modal.getInstance(document.getElementById('foodModal'));
                                if (foodModal) {
                                    foodModal.hide();
                                } else {
                                    console.warn("⚠ Bootstrap モーダルのインスタンスが取得できませんでした。");
                                }

                                foodResults.innerHTML = ""; // 🔹 検索結果をクリア

                            };
                            foodResults.appendChild(li);
                        });
                    })
                    .catch(error => console.error("❌ エラー発生:", error));  // 🔍 エラーハンドリング
            } else {
                foodResults.innerHTML = "";
            }
        });
    }

    // **🔹 画像モーダルの初期設定**
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const closeBtn = document.querySelector(".close");

    if (modal && modalImg && closeBtn) {
        // **ページロード時にモーダルを非表示にする**
        modal.style.display = "none";

        // **画像をクリックでモーダルを開く**
        document.querySelectorAll(".review-thumbnail").forEach(img => {
            img.addEventListener("click", function(event) {
                event.stopPropagation();  // **クリックイベントの伝播を防ぐ**
                modal.style.display = "flex"; // `flex` を適用し中央表示
                modalImg.src = this.src;
            });
        });

        // **モーダルを閉じる**
        closeBtn.addEventListener("click", function() {
            modal.style.display = "none";
        });

        window.addEventListener("click", function(event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    }

});
