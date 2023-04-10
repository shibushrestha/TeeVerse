const addToCartBtn = document.querySelectorAll(".addToCart");
addToCartBtn.forEach(btn =>{
    btn.addEventListener('click', function(e){
        e.preventDefault()
        let productId = this.dataset.product;
        let user = this.dataset.user;
        console.log(user)
        console.log(productId)
        if(user === "AnonymousUser"){
            window.location.href = `/Myapp/login/?next=${location.pathname}`;
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

                const navWrapper = document.querySelector(".navbar-wrapper")
                navWrapper.appendChild(newP);

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
