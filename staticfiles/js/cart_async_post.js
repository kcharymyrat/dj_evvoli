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
        try {
            const response = await fetch(addURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            if(response.ok) {
                console.log(response.json)
                const jsonData = await response.json();
                updateDisplay(jsonData.productQty);
                updateNavCart(jsonData.cartQty);
            } else {
                console.log(response.json)
                console.error('Failed to add item to cart');
            }
        } catch (error) {
            console.error('Failed to connect to server', error);
        }
    };

    // Remove from cart function
    const removeFromCart = async () => {
        try {
            const response = await fetch(removeURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });
            if(response.ok) {
                console.log(response.json)
                const jsonData = await response.json();
                updateDisplay(jsonData.productQty);
                updateNavCart(jsonData.cartQty);
            } else {
                console.log(response.json)
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

    console.log("END OF SCRIPT")
});


// window.addEventListener('popstate', function(event) {
//     console.log("in popstate", event)

//     // Refresh your page elements here
//     navCart = document.querySelector('#cart-qty');
//     addBtn = document.querySelector('#add-btn');
//     minusBtn = document.querySelector('#d-none-minus-btn');
//     plusBtn = document.querySelector('#d-none-plus-btn');
//     qtyDisplay = document.querySelector(`#d-none-product-qty`);
//     dNoneDiv = document.querySelector('#d-none-div');

//     addURL = addBtn.dataset.url;
//     removeURL = minusBtn.dataset.url;

//     productQty = addBtn.dataset.productQty;
//     cartQty = addBtn.dataset.cartQty;

//     updateDisplay(productQty);
// });

// console.log("END OF cart_async_post.js SCRIPT")