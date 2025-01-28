document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.favorite-button');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); //CSRFトークンを利用

    buttons.forEach(button => {
        button.addEventListener('click', async () => {
            const foodId =button.dataset.foodId;

            try {
                const response = await fetch(`/favorite/toggle/${foodId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken, //CSRFトークンをヘッダーに追加
                    },
                });

                const result = await response.json();

                if  (result.status === 'added') {
                    button.textContent = 'お気に入りから削除';
                    alert(result.message);
                } else if (result.status === 'removed') {
                    button.textContent = 'お気に入りに追加';
                    alert(result.message);
                } else {
                    alert('エラーが発生しました');
                }
            } catch (error) {
                console.error('エラー:', error);
                alert('リクエストに失敗しました');
            }
        });            
    });
});
