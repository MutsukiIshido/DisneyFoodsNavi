document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.favorite-button');

    // 画面読み込み時にボタンの状態を設定
    buttons.forEach(button => {
        const isFavorited = button.dataset.favorited === 'true';
        updateButton(button, isFavorited);
    });

    buttons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            if (!window.isLoggedIn) {
                window.location.href = '/login/';
                return;
            }

            const foodId = this.dataset.foodId;

            fetch(`/favorite/toggle/${foodId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(data => {
                const isFavorited = data.status === 'added'; // 追加 or 削除を判定
                updateButton(this, isFavorited); // ボタン見た目を更新
            })
            .catch(error => {
                console.error('エラー:', error);
                alert('リクエストに失敗しました');
            });
        });
    });

    // ボタンの見た目を更新する関数
    function updateButton(button, isFavorited) {
        if (isFavorited) {
            button.classList.add('favorited');
            button.innerHTML = '❤️ お気に入り解除';
            button.dataset.favorited = 'true';
        } else {
            button.classList.remove('favorited');
            button.innerHTML = '🧡 お気に入り追加';
            button.dataset.favorited = 'false';
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
