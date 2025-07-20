var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        // Kiểm tra biến user có tồn tại
        if (typeof user !== 'undefined') {
            if (user === "AnonymousUser") {
                console.log('User not logged in')
            } else {
                updateUserOrder(productId, action)
            }
        } else {
            console.log('Biến user chưa được định nghĩa trong template')
        }
    })
}
function updateUserOrder(productId, action) {
    console.log('User logged in, sending data...')
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',  
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken 
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })  
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()  
    })
}
