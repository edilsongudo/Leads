//Logic 1
const pickr = Pickr.create({
    el: '.color-picker',
    theme: 'nano',
    default: color1,

    components: {

        preview: true,
        hue: true,

        interaction: {
            save: true
        }
    }
});

const pickr2 = Pickr.create({
    el: '.color-picker2',
    theme: 'nano',
    default: color2,

    components: {

        preview: true,
        hue: true,

        interaction: {
            save: true
        }
    }
});

const pickr3 = Pickr.create({
    el: '.color-picker3',
    theme: 'nano',
    default: color3,

    components: {

        preview: true,
        hue: true,
        opacity: true,

        interaction: {
            save: true
        }
    }
});

// const pickr4 = Pickr.create({
//     el: '.color-picker4',
//     theme: 'nano',
//     default: color4,

//     components: {

//         preview: true,
//         hue: true,

//         interaction: {
//             save: true
//         }
//     }
// });

pickr.on('save', (...args) => {
    let color = args[0].toRGBA().toString(3);
    let color1_input = document.getElementById('color1')
    color1_input.value = color
});

pickr2.on('save', (...args) => {
    let color2 = args[0].toRGBA().toString(3);
    let color2_input = document.getElementById('color2')
    color2_input.value = color2
});
pickr3.on('save', (...args) => {
    let color3 = args[0].toRGBA().toString(3);
    let color3_input = document.getElementById('link_background_color')
    color3_input.value = color3
});
// pickr4.on('save', (...args) => {
//     let color4 = args[0].toRGBA().toString(3);
//     let color4_input = document.getElementById('link_text_color')
//     color4_input.value = color4
// });
let rangeInputs = document.querySelectorAll('.range-input input')
rangeInputs.forEach(function(rangeInput) {
    rangeInput.addEventListener("input",function(){
    rangeInput.parentElement.childNodes[5].innerHTML = '<div>' + rangeInput.value + '</div>'
    });
})

//Logic 2
let options = document.querySelectorAll('.font')
options.forEach(function(elem) {
    new_font = new FontFace(elem.parentElement.children[0].value.split('.')[0], `url(/media/fonts/${elem.parentElement.children[0].value})`)
    new_font.load().then(function(loaded_face) {
        document.fonts.add(loaded_face)
        elem.style.fontFamily = elem.parentElement.children[0].value.split('.')[0]
    }).catch(function(error) {
        console.log(error)
    });
})
const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const input_font = document.querySelector("#font_input")
const optionsList = document.querySelectorAll(".option");

selected.style.fontFamily = font_family.split('.')[0]

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");
});

optionsList.forEach(o => {
  o.addEventListener("click", () => {
    selected.innerHTML = o.querySelector("label").innerHTML;
    input_font.value = o.querySelector("label").innerHTML;
    selected.style.fontFamily = input_font.value.split('.')[0]
    optionsContainer.classList.remove("active");
  });
});

//Logic 3
const useimageorcolor = document.querySelector('form')
useimageorcolor.addEventListener('change', function () {
    radio = document.querySelector('input[name="use_background_image"]:checked').value
    if (radio == 'false') {
        document.querySelector('#brightness_container').style.opacity = 0
        document.querySelector('#brightness_container').style.display = 'none'
        document.querySelector('.colorsdivs1').style.opacity = 1
        document.querySelector('.colorsdivs1').style.display = 'flex'
        document.querySelector('#colorsdiv1label').style.display = 'inline'
        document.querySelector('.imagesinputs').style.opacity = 0
        document.querySelector('.imagesinputs').style.display = 'none'
    } else {
        document.querySelector('#brightness_container').style.opacity = 1
        document.querySelector('#brightness_container').style.display = 'flex'
        document.querySelector('.colorsdivs1').style.opacity = 0
        document.querySelector('.colorsdivs1').style.display = 'none'
        document.querySelector('#colorsdiv1label').style.display = 'none'
        document.querySelector('.imagesinputs').style.opacity = 1
        document.querySelector('.imagesinputs').style.display = 'flex'
    }
})

//Logic 4
btn = document.querySelector('.desktopbtn')
image_input = document.querySelector('#id_background_image_desktop')
preview_image = document.querySelector('#desktopimage')
preview_image.style.backgroundImage = `url(/media/usersbackgroundimages/${desktopimage.split("/")[3]})`

btn.addEventListener('click', function (e) {
    e.preventDefault()
    image_input.click()
})

image_input.addEventListener('change', function() {

    // console.log(this.files[0])
    const file = this.files[0]

    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            const result = reader.result
            preview_image.style.backgroundImage = `url(${reader.result})`
        }

    reader.readAsDataURL(file)
    }
})

btn2 = document.querySelector('.mobilebtn')
image_input2 = document.querySelector('#id_background_image_mobile')
preview_image2 = document.querySelector('#mobileimage')
preview_image2.style.backgroundImage = `url(/media/usersbackgroundimages/${mobileimage.split("/")[3]})`

btn2.addEventListener('click', function (e) {
    e.preventDefault()
    image_input2.click()
})

image_input2.addEventListener('change', function() {

    // console.log(this.files[0])
    const file2 = this.files[0]

    if (file2) {
        const reader2 = new FileReader();
        reader2.onload = function () {
            const result2 = reader2.result
            preview_image2.style.backgroundImage = `url(${reader2.result})`
        }

    reader2.readAsDataURL(file2)
    }
})

//Logic 5
if (use_background_image == true) {
    document.querySelectorAll('input[name="use_background_image"]')[0].click()
} else {
    document.querySelectorAll('input[name="use_background_image"]')[1].click()
}


//Logic 6
document.querySelector('#togglepreviewbtn').addEventListener('click', function() {
    document.querySelector('#previewlanding').style.display = 'block'
    document.querySelector('#preferences').style.display = 'none'
})

document.querySelector('#togglepreferencesbtn').addEventListener('click', function() {
    document.querySelector('#previewlanding').style.display = 'none'
    document.querySelector('#preferences').style.display = 'block'
})
