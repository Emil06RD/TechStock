
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('productForm');

  if (form) {
    form.addEventListener('submit', function (e) {
      let valid = true;

      const nameInput = document.getElementById('productName');
      const priceInput = document.getElementById('productPrice');
      const quantityInput = document.getElementById('productQuantity');
      const categorySelect = document.getElementById('productCategory');


      [nameInput, priceInput, quantityInput, categorySelect].forEach(el => {
        el.classList.remove('is-invalid');
      });


      if (!nameInput.value.trim()) {
        nameInput.classList.add('is-invalid');
        valid = false;
      }


      const priceVal = parseFloat(priceInput.value);
      if (priceInput.value === '' || isNaN(priceVal) || priceVal < 0) {
        priceInput.classList.add('is-invalid');
        valid = false;
      }


      const qtyVal = parseInt(quantityInput.value, 10);
      if (quantityInput.value === '' || isNaN(qtyVal) || qtyVal < 0 || !Number.isInteger(parseFloat(quantityInput.value))) {
        quantityInput.classList.add('is-invalid');
        valid = false;
      }


      if (!categorySelect.value) {
        categorySelect.classList.add('is-invalid');
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
      } else {
        const saveBtn = document.getElementById('saveProductBtn');
        if (saveBtn) {
          saveBtn.disabled = true;
          saveBtn.textContent = 'Guardando...';
        }
      }
    });
  }
});
