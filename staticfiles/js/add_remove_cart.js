let isClickable = true;
const btnDisableTime = 500; // ms

let itemsInCart = 0 //`{{ request.session.cart_qty|default:0 }}`
let productQtyInCart = 0 // `{{ product_qty_in_cart|default:0 }}`
console.log("itemsInCart =", itemsInCart)
console.log("productQtyInCart =", productQtyInCart)

const addBtn = document.querySelector('#add-btn')
const dNoneDiv = document.querySelector('#d-none-div')
const dNoneMinusBtn = document.querySelector('#d-none-minus-btn')
const dNonePElemProductQty = document.querySelector('#d-none-product-qty')
const dNonePlusBtn = document.querySelector('#d-none-plus-btn')

console.log("addBtn =", addBtn)
console.log("dNoneDiv =", dNoneDiv)
console.log("dNoneMinusBtn =", dNoneMinusBtn, "dNonePElemProductQty =", dNonePElemProductQty, "dNonePlusBtn =", dNonePlusBtn)

document.querySelector("#product-detail-div").addEventListener('click', function(event) {
  var clickedElementId = event.target.id;
  console.log('You clicked on: ', clickedElementId);
});

function updateProductQtyInElement(e) {
  // Update the displayed product count
  e.textContent = productQtyInCart;
};

const addAndUpdateCartProducts = (eQtyToBeUpdated, eToAddDNone, eToRemoveDNone) => {
  updateProductQtyInElement(eQtyToBeUpdated);
  
  if (productQtyInCart > 0) {
    eToAddDNone.classList.add('d-none');
    eToRemoveDNone.classList.remove('d-none');
  };
};


const removeAndUpdateCartProducts = (eQtyToBeUpdated, eToAddDNone, eToRemoveDNone) => {
  updateProductQtyInElement(eQtyToBeUpdated);
  
  if (productQtyInCart === 0) {
    eToAddDNone.classList.add('d-none');
    eToRemoveDNone.classList.remove('d-none');
  };
};

addBtn.addEventListener("click", () => {
  // Disable the button immediately after it's clicked
  addBtn.disabled = true;

  // Increase the product count in cart
  console.log("productQtyInCart =", productQtyInCart)
  productQtyInCart++;
  console.log("productQtyInCart =", productQtyInCart)
  
  addAndUpdateCartProducts(
    eQtyToBeUpdated=dNonePElemProductQty, 
    eToAddDNone=addBtn, 
    eToRemoveDNone=dNoneDiv
  )
  console.log("addBtn =", addBtn)

  // Re-enable the button after 1 second (or however long you want to wait)
  setTimeout(() => {
      addBtn.disabled = false;
  }, btnDisableTime); // ms
});


dNoneMinusBtn.addEventListener("click", () => {
  // Decrease the product count, but not below 0
  productQtyInCart = Math.max(productQtyInCart - 1, 0);

  dNoneMinusBtn.disabled = true;
  
  removeAndUpdateCartProducts(
    eQtyToBeUpdated=dNonePElemProductQty, 
    eToAddDNone=dNoneDiv, 
    eToRemoveDNone=addBtn
  )

  // Re-enable the button after 1 second (or however long you want to wait)
  setTimeout(() => {
    dNoneMinusBtn.disabled = false;
  }, btnDisableTime); // 1000 ms = 1 second
});

dNonePlusBtn.addEventListener("click", () => {
  // Increase the product count in cart
  productQtyInCart++;
  updateProductQtyInElement(dNonePElemProductQty);
  dNonePlusBtn.disabled = true;
  dNonePlusBtn.classList.add('d-none');
  setTimeout(() => {
    dNonePlusBtn.disabled = false;
  }, 3000); // 1000 ms = 1 second
  console.log("clicked");
  dNonePlusBtn.classList.remove('d-none');
});