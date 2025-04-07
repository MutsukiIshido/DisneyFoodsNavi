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
            const modal = new bootstrap.Modal(document.getElementById('foodModal'), {
                backdrop: false
            });
            modal.show();
        });
    }

    // 🔹 商品検索機能
    const foodSearchInput = document.getElementById('foodSearch');
    const foodResults = document.getElementById('foodResults');
    const foodField = document.getElementById('id_food');
    const foodDisplay = document.getElementById('food_display');

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

    if (foodSearchInput) {
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
                            li.onclick = () => {
                                console.log("✅ food.id:", food.id);  // ←ここ追加！

                                foodField.value = food.id;
                                foodDisplay.value = food.name;
    
                                // モーダル閉じる
                                const foodModal = bootstrap.Modal.getInstance(document.getElementById('foodModal'));
                                if (foodModal) foodModal.hide();
    
                                foodResults.innerHTML = "";
    
                                // 🔥 商品に紐づく店舗を取得してselectを更新
                                fetch(`/api/get-stores-for-food/?food_id=${food.id}`)
                                    .then(res => res.json())
                                    .then(stores => {
                                        const storeSelect = document.getElementById("id_store");
                                        storeSelect.innerHTML = ""; // クリア
    
                                        stores.forEach(store => {
                                            const option = document.createElement("option");
                                            option.value = store.id;
                                            option.textContent = store.name;
                                            storeSelect.appendChild(option);
                                        });
    
                                        if (stores.length === 0) {
                                            const option = document.createElement("option");
                                            option.textContent = "該当する店舗がありません";
                                            option.disabled = true;
                                            option.selected = true;
                                            storeSelect.appendChild(option);
                                        }
                                    });
                            };
                            foodResults.appendChild(li);
                        });
                    });
            } else {
                foodResults.innerHTML = "";
            }
        });
    }
});
