var preview_image = document.querySelector('#desktopimage')
preview_image.style.backgroundImage = `url(/media/usersbackgroundimages/${desktopimage.split("/")[3]})`
var basic = initcropper(256, 144, 'square')
var btn = document.querySelector('.desktopbtn')
var image_input = document.querySelector('#id_background_image_desktop')
handle_file_crop(basic, btn, image_input, preview_image, '/desktop/upload/', '.modal', '#cropbutton', 'original')


var preview_image2 = document.querySelector('#mobileimage')
preview_image2.style.backgroundImage = `url(/media/usersbackgroundimages/${mobileimage.split("/")[3]})`
var basic2 = initcropper2(144, 256, 'square')
var btn2 = document.querySelector('.mobilebtn')
var image_input2 = document.querySelector('#id_background_image_mobile')
handle_file_crop(basic2, btn2, image_input2, preview_image2, '/mobile/upload/', '.modal2', '#cropbutton2', 'original')

