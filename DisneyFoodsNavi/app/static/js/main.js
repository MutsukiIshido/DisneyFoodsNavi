document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScriptが読み込まれました');

    document.getElementById('openFoodSearch').addEventListener('click', () => {
        event.preventDefault(); // フォームの送信を防ぐ
        console.log('ボタンがクリックされました'); 
        const width = 600;
        const height = 400;
        const left = (window.screen.width - width) / 2;
        const top = (window.screen.height - height) / 2;
        const popup = window.open('/food-search/', '商品検索', `width=${width},height=${height},top=${top},left=${left}`);        
        if (popup) {
            console.log('ポップアップが開きました');
        } else {
            console.error('ポップアップがブロックされました');
        }

        // モーダルを表示
        const modal = new bootstrap.Modal(document.getElementById('foodModal'));
        modal.show();
    });
});