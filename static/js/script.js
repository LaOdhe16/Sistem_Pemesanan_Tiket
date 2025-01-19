console.log("Sistem Pemesanan Tiket aktif!");

// Animasi hover untuk tombol
const buttons = document.querySelectorAll('button');
buttons.forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.style.backgroundColor = '#45a049';
    });
    button.addEventListener('mouseleave', () => {
        button.style.backgroundColor = '#388E3C';
    });
});
