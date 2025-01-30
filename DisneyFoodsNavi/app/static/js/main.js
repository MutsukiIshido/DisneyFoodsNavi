document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScriptが読み込まれました');

    // フォームのリセットが発生するかチェック
    const form =document.querySelector("form"); // <form>要素を取得
    if (form) {
        form.addEventListener("reset", () => {
            console.log("🚨 フォームがリセットされました！ 🚨");
        });
    }

    // 商品検索ボタンの処理
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

    // 検索機能の処理
    const foodSearchInput = document.getElementById('foodSearch');
    const foodResults = document.getElementById('foodResults');
    const foodField = document.getElementById('id_food');
    console.log("foodField の値:", foodField);

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
                            // 商品選択時の処理
                            foodResults.appendChild(li);
                            li.onclick = () => {
                                console.log("クリックされた食品:", food.name);

                                // 商品名をフォームフィールドにセット
                                foodField.value = food.name;  
                                console.log("設定後の foodField.value:", foodField.value);

                                // モーダルを閉じる
                                const modal = bootstrap.Modal.getInstance(document.getElementById('foodModal'));
                                modal.hide(); 

                                console.log("モーダル閉じた後の foodField.value:", foodField.value);
                            };
                            // foodResults.appendChild(li);
                        });
                    });
            } else {
                foodResults.innerHTML = '';
            }
        });
    }
});