const numberInput = document.getElementById('orderQty');
numberInput.style['-webkit-appearance'] = 'textfield';
numberInput.style['-moz-appearance'] = 'textfield';


let quantity = document.getElementById('orderQty').value;
console.log(quantity);


function addQty(){
    if(quantity < 5){
        document.getElementById('subQty').style.cursor = 'auto';
        quantity++;
        console.log(quantity);
        document.getElementById('orderQty').value = quantity;
    }else if(quantity === 5){
        document.getElementById('addQty').style.cursor = 'no-drop';
        console.log('You connot order more than 5 items.')
        return;
    }
};


function subQty(){
    if(quantity > 1){
        document.getElementById('addQty').style.cursor = 'auto';
        quantity--;
        console.log(quantity);
        document.getElementById('orderQty').value = quantity;
    }else if(quantity === 1){
        document.getElementById('subQty').style.cursor = 'no-drop';
        console.log('You cannot order less than 1 item.')
        return;
    }
};

    
const addToCartBtn = document.querySelectorAll(".addToCart");
addToCartBtn.forEach(btn =>{
    btn.addEventListener('click', function(e){
        e.preventDefault()
        let productId = this.dataset.product;
        let user = this.dataset.user;
        console.log(user)
        console.log(productId)
        // When the user clicks on the add to cart button, check that the user is authenticated or not
        // If the user is not authenticated,
        // we will send the user to the login page with the next parameter set to the current page the user was.
        if(user === "AnonymousUser"){
            const login_url = `/Myapp/login/?next=${window.location.pathname}`;
            window.location.href = login_url;
        }
        // If the user is authenticated, we will do a post request using fetch api and add the product to the cart
        else{
            url = "/Myapp/cart/"
            fetch(url,{
                method:'POST',
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type':'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({'productId':productId}),
                credentials: 'same-origin'

            })
            .then((response) => {
                if(response.ok){
                    location.reload();
                }else{
                    console.error('failed to redirect.');
                }
            })
            .catch(error =>{
                console.error('Error while redirecting', error);
            })
        }
    })
});


 // Hide the success message after 5 seconds
 setTimeout(function() {
    let successMessage = document.getElementById('successMsg');
    if (successMessage) {
        successMessage.style.display = "none";
    }
}, 2000);

