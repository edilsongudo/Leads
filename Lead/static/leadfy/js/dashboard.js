function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    $(document).ready(function() {
        // var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
        const csrfToken = getCookie('csrftoken');
        dict = {"request": "Hello from JS." }
        var data = JSON.stringify(dict)

        $.ajax({
            url: '',
            headers: {'X-CSRFToken': csrfToken},
            dataType: 'json',
            data: data,
            type: 'post',
            success: function(response) {
                console.log(response)
                var p = document.getElementById('page_views_count')
                var l = document.getElementById('number_of_leads')
                p.innerHTML = response.page_views
                l.innerHTML = response.number_of_leads

                const data = {
                  labels: response.labels,
                  datasets: [
                  {
                    label: 'Unique Link Views',
                    fill: true,
                    lineTension: 0.1,
                    backgroundColor: '#A6A6F0',
                    borderColor: 'rgb(48, 112, 212)',
                    // borderCapStyle: 'butt',
                    // borderDash: [],
                    // borderDashOffset: 0.0,
                    // borderJoinStyle: 'miter',
                    // pointBorderColor: '#fff',
                    // pointBorderWidth: 1,
                    // pointHoverRadius: 5,
                    // pointHoverBackgroundColor: '#fff',
                    // pointHoverBorderColor: '#fff',
                    // pointHoverBorderWidth: 2,
                    //pointRadius: 1,
                    //pointHitRadius: 10,
                    data: response.clicks_per_hours,
                  },
                  ]
                };

                const config = {
                  type: 'line',
                  data,
                  options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                  }
                };

              // === include 'setup' then 'config' above ===
                  var myChart = new Chart(
                    document.getElementById('myChart'),
                    config
                  );

                  var piechart = new Chart(
                    document.getElementById('piechart'), {
                        type: 'radar',
                        data: {
                            labels: response.channels,
                            datasets: [
                                {
                                    label: 'Visits',
                                    borderColor: '#A6A6F0',
                                    borderWidth: 2,
                                    data: response.visits
                                }
                            ]
                        }
                    })

            }
                })

        });

// window.onhashchange = function (argument) {
//     alert(window.location.hash)
// }

var pageURL = window.location.pathname
pageURL = pageURL.split('/')
console.log(pageURL)
var lastURLSegment = pageURL[2]
console.log(lastURLSegment)
// var lastURLSegment = pageURL.substr(pageURL.lastIndexOf('/') -2 )
// console.log(lastURLSegment)
// lastURLSegment = lastURLSegment.replace('/', '')
// console.log(lastURLSegment)

var card_day = document.getElementById(lastURLSegment)
card_day.classList.add('active')
console.log(card_day)

