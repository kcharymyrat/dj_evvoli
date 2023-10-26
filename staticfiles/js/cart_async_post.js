// console.log("cart_asyn_post.js")

window.addEventListener('DOMContentLoaded', (event) => {
    // console.log("window.addEventListener")

    const navCart = document.querySelector('#cart-qty');
    // console.log("navCart =", navCart);

    const addBtn = document.querySelector('#add-btn');
    const minusBtn = document.querySelector('#d-none-minus-btn');
    const plusBtn = document.querySelector('#d-none-plus-btn');
    const qtyDisplay = document.querySelector(`#d-none-product-qty`);
    const dNoneDiv = document.querySelector('#d-none-div');

    let addURL = addBtn.dataset.url;
    let removeURL = minusBtn.dataset.url;

    let productQty = addBtn.dataset.productQty;
    let cartQty = addBtn.dataset.cartQty;

    // console.log(addURL, removeURL)
    // console.log("cartQty =", cartQty, "productQty =", productQty)

    // Function to update the display and button visibility
    const updateDisplay = (qty) => {
        // console.log("qty =", qty)
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
        const response = await fetch(addURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();
        updateDisplay(data.productQty);
        updateNavCart(data.cartQty);
    };

    // Remove from cart function
    const removeFromCart = async () => {
        const response = await fetch(removeURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();
        updateDisplay(data.productQty);
        updateNavCart(data.cartQty);
    };

    // Event handlers
    addBtn.addEventListener('click', addToCart);
    minusBtn.addEventListener('click', removeFromCart);
    plusBtn.addEventListener('click', addToCart);

    console.log("END OF SCRIPT")
});


