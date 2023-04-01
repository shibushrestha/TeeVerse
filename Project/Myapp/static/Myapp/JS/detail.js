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