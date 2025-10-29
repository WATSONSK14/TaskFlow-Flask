// Flash mesajları için JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Tüm flash mesajlarını bul
    const flashMessages = document.querySelectorAll('.flash-message, .form-flash-message');
    
    flashMessages.forEach(function(message) {
        // Kapatma butonu ekle
        addCloseButton(message);
        
        // 2 saniye sonra otomatik kapat
        setTimeout(function() {
            closeMessage(message);
        }, 2000);
    });
});

function addCloseButton(message) {
    // Kapatma butonu oluştur
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.className = message.classList.contains('form-flash-message') ? 'form-flash-close' : 'flash-close';
    closeButton.setAttribute('aria-label', 'Mesajı kapat');
    
    // Tıklama olayı ekle
    closeButton.addEventListener('click', function() {
        closeMessage(message);
    });
    
    // Butonu mesaja ekle
    message.appendChild(closeButton);
}

function closeMessage(message) {
    // Kapanma animasyonu başlat
    message.classList.add('closing');
    
    // Animasyon bitince elementi kaldır
    setTimeout(function() {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 300); // CSS transition süresi ile aynı
}
