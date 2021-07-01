var priceEl = document.querySelector('#price')
var upwEl = document.querySelector('#upw')
var devEl = document.querySelector('#dev')
var kevEl = document.querySelector('#kev')
var hanEl = document.querySelector('#han')
var price
var remaining

function calculate () {
    price = Number(priceEl.value)

    // Calc Upwork Gain
    if (price <= 500) {
        upwEl.value = `$${(Number(priceEl.value) * 0.8).toFixed(2)}`
        remaining = Number(priceEl.value) - Number(priceEl.value) * 0.2
    } else {
        upwEl.value = `$${(price * 0.9).toFixed(2)}`
        remaining = Number(priceEl.value) - Number(priceEl.value) * 0.1
    }

    // Calc Dev Gains
    devEl.value = `$${(remaining * 0.65).toFixed(2)}`
    remaining = remaining - remaining * 0.65

    // Calc Kev Gains
    kevEl.value = `$${(remaining * 0.55).toFixed(2)}`
    remaining = remaining * 0.45

    // Calc Han Gains
    hanEl.value = `$${remaining.toFixed(2)}`
}

calculate()
priceEl.addEventListener('change', calculate)
