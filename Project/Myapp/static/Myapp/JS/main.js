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
        if(user === "AnonymousUser"){
            window.location.href = "/Myapp/login/"
        } else {
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
            .then(res => res.json())
            .then((data)=>{
                message = JSON.parse(data['message'])
                const newP = document.createElement('p')
                const successMsgId = 'successMsg-' + productId;
                newP.id = successMsgId;
                newP.className = 'successMsg';
                newP.textContent = message;
                document.body.appendChild(newP);

                // Hide the success message after 2 seconds
                let lastSuccessMsg = null; // Keep track of the most recently added success message
                setTimeout(function() {
                    if (lastSuccessMsg) { // Hide the most recently added success message
                        lastSuccessMsg.style.display = "none";
                        lastSuccessMsg = null; // Reset lastSuccessMsg so it doesn't hide the wrong element later
                    }
                }, 2000);
                lastSuccessMsg = newP; // Update lastSuccessMsg to the newly added success message
            })
        }
    })
});

