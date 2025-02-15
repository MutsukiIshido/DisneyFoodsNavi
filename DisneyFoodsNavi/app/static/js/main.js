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
