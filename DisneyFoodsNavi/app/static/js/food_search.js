document.addEventListener('DOMContentLoaded', () => {
    const foodSearchInput = document.getElementById('foodSearch');
    const foodResults = document.getElementById('foodResults');
    const foodField = document.getElementById('id_food');

    // 入力時に検索処理
    foodSearchInput.addEventListener('input', function () {
        const query = this.value.trim();
        if (query) {
            fetch(`/food-search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    foodResults.innerHTML = '';
                    data.forEach(food => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item';
                        li.textContent = food.name;
                        li.onclick = () => {
                            foodField.value = food.name; // フィールドに反映
                            const modal = bootstrap.Modal.getInstance(document.getElementById('foodModal'));
                            modal.hide(); // モーダルを閉じる
                        };
                        foodResults.appendChild(li);
                    });
                });
        } else {
            foodResults.innerHTML = '';
        }
    });
});
