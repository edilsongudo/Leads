const links = document.querySelector('#links')
Sortable.create(links, {
    group: {name: 'mylinks'},
    animation: 300,
    easing: 'cubic-bezier(0.895, 0.03, 0.685, 0.22)',
    handle: '.fa-grip-lines',
    store: {
        set: function(links) {
            const order = links.toArray()
            submitorder('links', order, '')
        }
    }
})

function submitorder(dataname, datavalue, url) {
    dict = {data: datavalue}
    var csrfToken = getCookie('csrftoken')
    console.log(csrfToken)
    var json = JSON.stringify(dict)
    console.log(json)

     $.ajax({
        url: url,
        headers: {'X-CSRFToken': csrfToken},
        dataType: 'json',
        data: json,
        type: 'post',
        success: function(response) {
            console.log('Response: ', response)
        }
    })
}

const button = document.querySelector('#copybtn')
button.addEventListener('click', function () {
    const inputelem = document.createElement('textarea')
    inputelem.value = link
    document.body.appendChild(inputelem)
    console.log(inputelem.value)
    inputelem.select()
    document.execCommand('Copy')
    document.body.removeChild(inputelem)

    button.innerHTML = 'Link Copied <i class="fas fa-check">'
    button.style.color = "#eecda3"

    setTimeout(function () {
        button.innerHTML = 'Copy Link <i class="fas fa-copy">'
        button.style.backgroundColor = 'white'
        button.style.color = "grey"
    }, 2500)
})



