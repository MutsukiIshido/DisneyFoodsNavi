document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScriptが読み込まれました');

    // 🔹 ドロップダウンメニュー制御
    const dropdownToggle = document.querySelector(".dropdown-toggle");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    if (dropdownToggle && dropdownMenu) {
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
    }

    // 🔹 フォームのリセットチェック
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("reset", () => {
            console.log("🚨 フォームがリセットされました！ 🚨");
        });
    }

    // 🔹 商品検索機能とモーダル処理
    const foodSearchInput = document.getElementById('foodSearch');
    const foodResults = document.getElementById('foodResults');
    const foodField = document.getElementById('id_food');
    const foodDisplay = document.getElementById('food_display');

    if (foodSearchInput && foodResults && foodField && foodDisplay) {
        foodSearchInput.addEventListener("input", function () {
            const query = this.value.trim();
            if (query.length > 0) {
                fetch(`/food-search/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        foodResults.innerHTML = "";
                        if (data.length === 0) {
                            foodResults.innerHTML = "<li class='list-group-item'>該当なし</li>";
                            return;
                        }

                        data.forEach(food => {
                            const li = document.createElement("li");
                            li.className = "list-group-item list-group-item-action";
                            li.textContent = food.name;
                            li.dataset.foodId = food.id;

                            li.addEventListener("click", () => {
                                console.log("✅ food.id:", food.id);

                                // 選択したfoodのIDと名前をセット
                                foodField.value = food.id;
                                foodDisplay.value = food.name;

                                // モーダルを閉じる
                                const foodModal = bootstrap.Modal.getInstance(document.getElementById('foodModal'));
                                if (foodModal) foodModal.hide();

                                foodResults.innerHTML = "";

                                // 店舗選択を更新
                                updateStoreOptions(food.id);
                            });

                            foodResults.appendChild(li);
                        });
                    });
            } else {
                foodResults.innerHTML = "";
            }
        });
    }

    // 🔹 商品に対応する店舗リストを取得してselectを更新
    function updateStoreOptions(foodId) {
        fetch(`/api/get-stores-for-food/?food_id=${foodId}`)
            .then(res => res.json())
            .then(stores => {
                const storeSelect = document.getElementById("id_store");
                if (!storeSelect) return;

                storeSelect.innerHTML = ""; // 一旦クリア

                if (stores.length === 0) {
                    const option = document.createElement("option");
                    option.textContent = "該当する店舗がありません";
                    option.disabled = true;
                    option.selected = true;
                    storeSelect.appendChild(option);
                } else {
                    stores.forEach(store => {
                        const option = document.createElement("option");
                        option.value = store.id;
                        option.textContent = store.name;
                        storeSelect.appendChild(option);
                    });
                }

                storeSelect.disabled = false; // 無効化されていた場合に備えて有効化
            });
    }

    // 🔹 レビュー画像モーダル（画像表示用）
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const closeBtn = document.querySelector(".close");

    if (modal && modalImg && closeBtn) {
        modal.style.display = "none";

        document.querySelectorAll(".review-thumbnail").forEach(img => {
            img.addEventListener("click", function(event) {
                event.stopPropagation();
                modal.style.display = "flex";
                modalImg.src = this.src;
            });
        });

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
