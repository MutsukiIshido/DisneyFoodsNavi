document.adddEventListener("DOMContentLoaded", function () {
    const dropdownToggle = document.querySelector(".dropdown-toggle");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    // 初期状態で非表示
    dropdownMenu.computedStyleMap.display = "none";

    dropdownToggle.addEventListener("click", function (event) {
        event.preventDefault(); // リンクのデフォルト動作を防ぐ
        if (dropdownMenu.computedStyleMap.display === "none") {
            dropdownMenu.computedStyleMap.display = "block"; // 表示
        } else {
            dropdownMenu.computedStyleMap.display = "none"; // 非表示
        }
    });

    // メニューをクリックしたら閉じる
    document.addEventListener("click", function (event) {
        if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = "none";
        }
    });
});