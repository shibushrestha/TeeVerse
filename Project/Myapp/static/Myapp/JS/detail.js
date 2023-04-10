const qtyInput = document.getElementById('orderQty');
qtyInput.style['-webkit-appearance'] = 'textfield';
qtyInput.style['-moz-appearance'] = 'textfield';

document.getElementById('subQty').style.cursor = 'pointer';
function addQty(){
    let quantity = qtyInput.value;
    if(quantity < 5){
        document.getElementById('subQty').style.cursor = 'pointer';
        quantity++;
        console.log(quantity);
        qtyInput.value = quantity;
    }else{
        document.getElementById('addQty').style.cursor = 'no-drop';
        console.log('You connot order more than 5 items.')
    }
};

document.getElementById('addQty').style.cursor = 'pointer';
function subQty(){
    let quantity = qtyInput.value;
    if(quantity > 1){
        document.getElementById('addQty').style.cursor = 'pointer';
        quantity--;
        console.log(quantity);
        qtyInput.value = quantity;
    }else{
        document.getElementById('subQty').style.cursor = 'no-drop';
        console.log('You cannot order less than 1 item.')
    }
};