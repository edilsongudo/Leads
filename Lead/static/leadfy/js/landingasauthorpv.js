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
    var csrf = document.getElementsByName('csrfmiddlewaretoken')
    var csrfToken = csrf[0].value
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
