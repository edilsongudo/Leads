var basic = initcropper(200, 200, 'circle')
var btn = document.querySelector('.clearbtnstyle')
var image_input = document.querySelector('#id_image')
var preview_image = document.querySelector('#round')
handle_file_crop(basic, btn, image_input, preview_image, 'upload/',  '.modal', '#cropbutton',  {'width': 200, 'height': 200}, 'png', 0.1)
