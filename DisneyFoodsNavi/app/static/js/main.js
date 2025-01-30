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
                                console.log("✅ クリックされた商品:", food.name);

                                const foodField = document.getElementById('id_food');
                                const foodDisplay = document.getElementById('food_display');
                                console.log("🔍 foodField の要素:", foodField);

                                if (!foodField) {
                                    console.error("🚨 foodField (id_food) が見つかりません！");
                                    return;
                                }
                                if (!foodDisplay) {
                                    console.error("🚨 foodDisplay (food_display) が見つかりません！");
                                    return;
                                }

                                // 商品名をセット
                                foodField.value = food.id;// 隠しフィールドにセット
                                foodDisplay.value = food.name; // ユーザー向けの表示用フィールドにセット
                                
                                console.log("🎯 設定後の foodField.value:", foodField.value);
                                console.log("🎯 設定後の foodDisplay.value:", foodDisplay.value);

                                console.log("🎯 foodField にセットした値:", foodField.value);


                                // `input` イベントを発火させる
                                foodField.dispatchEvent(new Event('change', { bubbles: true }));

                                // 0.5秒後の状態をチェック
                                setTimeout(() => {
                                    console.log("⌛ 0.5秒後の foodField.value:", foodField.value);
                                }, 500);

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

document.querySelector('form').addEventListener('submit', function(event) {
    const foodField = document.getElementById('id_food');
    console.log("🚀 送信直前の foodField.value:", foodField ? foodField.value : "⚠ foodField が見つかりません");
});


// document.querySelector('form').addEventListener('submit', function(event) {
//     event.preventDefault();  // 🔴 フォームの送信を一時的にキャンセル
//     console.log("🚀 フォーム送信がトリガーされました！");

//     const foodField = document.getElementById('id_food');
//     console.log("🚀 送信直前の foodField.value:", foodField ? foodField.value : "⚠ foodField が見つかりません");
// });


document.addEventListener('DOMContentLoaded', () => {
    console.log("📌 food のすべての要素:", document.querySelectorAll("[name='food']"));
});
