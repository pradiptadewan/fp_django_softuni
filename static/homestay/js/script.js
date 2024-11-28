// Smooth Scrolling for Internal Navigation
const navLinks = document.querySelectorAll('nav ul li a');

navLinks.forEach(link => {
  link.addEventListener('click', (event) => {
    const targetId = link.getAttribute('href');

    // Proses hanya ID internal yang dimulai dengan #
    if (targetId && targetId.startsWith('#')) {
      event.preventDefault(); // Menghentikan default action dari tautan

      const targetSection = document.querySelector(targetId);
      if (targetSection) {
        targetSection.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      } else {
        console.warn('Element not found:', targetId);
      }
    } else {
      // Jika href bukan ID internal, biarkan browser menangani navigasi default
      console.warn('Not an internal link:', targetId);
    }
  });
});

// Form Pencarian Kamar
const searchForm = document.querySelector('.room-search-form');

if (searchForm) {
  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();  // Mencegah form dari submit default
    const formData = new FormData(searchForm);
    const params = new URLSearchParams(formData).toString();

    // Validasi Form
    if (validateForm(formData)) {
      window.location.search = params; // Redirect dengan query params
    } else {
      console.warn('Form validation failed.');
    }
  });
} else {
  console.warn('Search form not found on the page.');
}

// Fungsi Validasi Form
function validateForm(formData) {
  let isValid = true;
  const checkInDate = new Date(formData.get('check_in'));
  const checkOutDate = new Date(formData.get('check_out'));

  // Elemen error untuk validasi
  const checkOutError = document.querySelector('#check_out_error');
  if (checkOutError) {
    if (checkOutDate <= checkInDate) {
      isValid = false;
      checkOutError.textContent = 'Tanggal check-out harus setelah tanggal check-in.';
      checkOutError.style.display = 'block';
    } else {
      checkOutError.textContent = '';
      checkOutError.style.display = 'none';
    }
  }
  return isValid;
}

// AJAX untuk Detail Kamar
const roomCards = document.querySelectorAll('.card');

roomCards.forEach(card => {
  const roomId = card.dataset.roomId;
  if (roomId) {
    card.addEventListener('click', (event) => {
      event.preventDefault();

      fetch(`/room/${roomId}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          const roomDetailsElement = document.getElementById('room-details');
          if (roomDetailsElement) {
            roomDetailsElement.innerHTML = `
              <h2>${data.name}</h2>
              <p>${data.description}</p>
              <img src="${data.image}" alt="${data.name}">
            `;
          } else {
            console.warn('Room details element not found.');
          }
        })
        .catch(error => {
          console.error('Error fetching room details:', error);
        });
    });
  } else {
    console.warn('No data-room-id found for this card.');
  }
});
