function initcropper (width, height, type, elem) {
    var basic = $(elem).croppie({
        viewport: {
            width: width,
            height: height,
            type: type
        },
    });
    return basic
}

function submitdata(response, url) {
    var csrf = document.getElementsByName('csrfmiddlewaretoken')
    var form = document.querySelectorAll('form')[1]
    var fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('cropped', response, 'image.png');

    $.ajaxSetup({async: false});
        $.ajax({
            type: 'POST',
            async: false,
            url: url,
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                alert('Success')
            },
            error: function(error){
                alert('Fail')
            },
            cache: false,
            contentType: false,
            processData: false,
        })
}



function handle_file_crop(basic, btn, image_input, preview_image, uploadURL) {
    btn.addEventListener('click', function (e) {
        e.preventDefault()
        console.log('Triggered')
        image_input.click()
    })

    image_input.addEventListener('change', function() {

        const file = this.files[0]

        if (file) {
            const reader = new FileReader();
            reader.onload = function () {
                const result = reader.result

                basic.croppie('bind', {
                    url: result,
                });
                // preview_image.style.backgroundImage = `url(${reader.result})`
            }

        reader.readAsDataURL(file)
        document.querySelector('.modal').style.display = 'flex'

        document.querySelector('#cropbutton').addEventListener('click', function() {

            basic.croppie('result', {type: 'blob', size: 'original'}).then(function(response) {
                preview_image.style.backgroundImage = `url(${URL.createObjectURL(response, {oneTimeOnly: true})})`
                document.querySelector('.modal').style.display = 'none'

                $('#submitbutton').click(function() {
                    submitdata(response, uploadURL)
                })

            });

        })

        }
    })

}
