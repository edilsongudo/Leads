function initcropper (width, height, type) {
    var basic = $('.demo').croppie({
        viewport: {
            width: width,
            height: height,
            type: type
        },
    });
    return basic
}

function initcropper2 (width, height, type) {
    var basic2 = $('.demo2').croppie({
        viewport: {
            width: width,
            height: height,
            type: type
        },
    });
    return basic2
}

function submitdata(response, url, filename) {
    var csrf = document.getElementsByName('csrfmiddlewaretoken')
    var form = document.querySelectorAll('form')[1]
    var fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value)

    fd.append('cropped', response, `${filename}.jpg`);

    $.ajaxSetup({async: false});
        $.ajax({
            type: 'POST',
            async: false,
            url: url,
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                console.log('Success')
            },
            error: function(error){
                console.log('Success')
            },
            cache: false,
            contentType: false,
            processData: false,
        })
}



function handle_file_crop(basic, btn, image_input, preview_image, uploadURL, container, cropbutton, size, format, quality) {
    btn.addEventListener('click', function (e) {
        e.preventDefault()
        image_input.click()
    })

    image_input.addEventListener('change', function() {

        const file = this.files[0]
        let filename = file.name.split('.')[0]

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const result = reader.result

                basic.croppie('bind', {
                    url: result,
                });
                // preview_image.style.backgroundImage = `url(${reader.result})`
            }

        reader.readAsDataURL(file)
        document.querySelector(container).style.display = 'flex'

        document.querySelector(cropbutton).addEventListener('click', function() {

            basic.croppie('result', {type: 'blob', size: size, format: format, quality: quality}).then(function(response) {
                preview_image.style.backgroundImage = `url(${URL.createObjectURL(response, {oneTimeOnly: true})})`
                document.querySelector(container).style.display = 'none'

                $('#submitbutton').click(function() {
                    submitdata(response, uploadURL, filename)
                })

            });

        })

        }
    })

}
