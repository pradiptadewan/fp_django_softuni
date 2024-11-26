// Smooth Scrolling for Internal Navigation
const navLinks = document.querySelectorAll('nav ul li a');

navLinks.forEach(link => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    const targetId = link.getAttribute('href');
    const targetSection = document.querySelector(targetId);

    // Smooth Scrolling with optional offset
    targetSection.scrollIntoView({ behavior: 'smooth', block: 'start',  // Adjust 'block' if needed
                                    inline: 'nearest' });
  });
});

// Pencarian Kamar: Mengambil form dan men-trigger pencarian dengan GET
const searchForm = document.querySelector('.room-search-form');

searchForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(searchForm);
  const params = new URLSearchParams(formData).toString();
  // Validasi Form
  if (validateForm(formData)) {
    window.location.search = params; // Mengarahkan ke URL dengan query params
  }
});

// Fungsi validasi form
function validateForm(formData) {
  let isValid = true;
  // Validasi field form (misalnya, pastikan check_in lebih awal dari check_out)
  // ...
  if (!isValid) {
    // Tampilkan pesan error di form
    alert('Harap lengkapi form pencarian dengan benar.');
  }
  return isValid;
}

// Fitur tambahan:
// 1. Menampilkan detail kamar dengan AJAX (tanpa reload halaman)
const roomCards = document.querySelectorAll('.card');

roomCards.forEach(card => {
  card.addEventListener('click', (event) => {
    event.preventDefault();
    const roomId = card.dataset.roomId; // Asumsikan ada atribut data-room-id

    // Panggil AJAX untuk mendapatkan detail kamar
    fetch(`/room/${roomId}`)
      .then(response => response.json())
      .then(data => {
        // Update elemen HTML dengan detail kamar
        // ...
      })
      .catch(error => {
        console.error('Error fetching room details:', error);
      });
  });
});

// 2. Mengatur slider gambar kamar (contoh: menggunakan Swiper.js)
// ... (Gunakan library seperti Swiper.js atau lainnya untuk implementasi slider)

// 3.  Implementasi modal untuk form booking (contoh: menggunakan Bootstrap Modal)
// ... (Gunakan library seperti Bootstrap Modal atau lainnya untuk implementasi modal)