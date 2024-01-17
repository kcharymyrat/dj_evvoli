window.addEventListener('DOMContentLoaded', (event) => {

    const navCart = document.querySelector('#cart-qty');

    const addBtn = document.querySelector('#add-btn');
    const minusBtn = document.querySelector('#d-none-minus-btn');
    const plusBtn = document.querySelector('#d-none-plus-btn');
    const qtyDisplay = document.querySelector(`#d-none-product-qty`);
    const dNoneDiv = document.querySelector('#d-none-div');

    let addURL = addBtn.dataset.url;
    let removeURL = minusBtn.dataset.url;

    let productQty = addBtn.dataset.productQty;
    let cartQty = addBtn.dataset.cartQty;

    var isClickAllowedProductDetail = true;
    function preventClicksTemporarilyProductDetail() {
        isClickAllowedProductDetail = false;
        setTimeout(() => {
            isClickAllowedProductDetail = true;
        }, 1000);
    }

    // Function to update the display and button visibility
    const updateDisplay = (qty) => {
        if (qty > 0) {
            addBtn.classList.add('d-none');
            dNoneDiv.classList.remove('d-none');
            qtyDisplay.textContent = qty;
        } else {
            addBtn.classList.remove('d-none');
            dNoneDiv.classList.add('d-none');
        }
    };

    const updateNavCart = (qty) => {
        navCart.textContent = qty;
    };

    // Initial update
    updateDisplay(productQty);

    // Add to cart function
    const addToCart = async () => {
        if (!isClickAllowedProductDetail) return;
        preventClicksTemporarilyProductDetail();
        try {
            const response = await fetch(addURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            if(response.ok) {
                const jsonData = await response.json();
                updateDisplay(jsonData.productQty);
                updateNavCart(jsonData.cartQty);
            } else {
                console.error('Failed to add item to cart');
            }
        } catch (error) {
            console.error('Failed to connect to server', error);
        }
    };

    // Remove from cart function
    const removeFromCart = async () => {
        if (!isClickAllowedProductDetail) return;
        preventClicksTemporarilyProductDetail();
        try {
            const response = await fetch(removeURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });
            if(response.ok) {
                const jsonData = await response.json();
                updateDisplay(jsonData.productQty);
                updateNavCart(jsonData.cartQty);
            } else {
                console.error('Failed to add item to cart');
            }
        } catch (error) {
            console.error('Failed to connect to server', error);
        }  
    };

    // Event handlers
    addBtn.addEventListener('click', addToCart);
    minusBtn.addEventListener('click', removeFromCart);
    plusBtn.addEventListener('click', addToCart);
});