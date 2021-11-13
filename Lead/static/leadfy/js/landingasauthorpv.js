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
const inputelem = document.querySelector('#copyinput')
button.addEventListener('click', function () {
    inputelem.select()
    document.execCommand('Copy')
    button.innerText = 'Link Copied'
    button.style.backgroundColor = 'rgba(48, 112, 212, 0.4)'
    button.style.color = "white"
})



