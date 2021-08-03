if (use_background_image == true) {

    //function to handle responsive images loading
    const mediaQuery = window.matchMedia('(max-width: 800px)')
    function handleTabletChange(e) {
        if (e.matches) {
            document.body.style.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,${brightness}), rgba(0,0,0,${brightness})), url(${mobileimage})`
        } else {
            document.body.style.backgroundImage = `linear-gradient(90deg, rgba(0,0,0,${brightness}), rgba(0,0,0,${brightness})), url(${desktopimage})`
        }
    }
    mediaQuery.addListener(handleTabletChange)
    handleTabletChange(mediaQuery)
    //end of function

} else {
    document.body.style.backgroundImage = `linear-gradient(90deg, ${color1}, ${color2})`
}

//Loading Font
new_font = new FontFace('customfont', `url(/media/fonts/${font})`)
new_font.load().then(function(loaded_face) {
    document.fonts.add(loaded_face)
    document.body.style.fontFamily = 'customfont'
    document.body.style.fontSize = primary_font_size + "px"
    document.getElementById('name').style.fontSize = name_font_size + "px"
}).catch(function(error) {
    console.log('Error loading font')
});
// End of Loading Font

let pages = document.querySelectorAll('.page-link') //Only querySelector Works!
pages.forEach(function(element, index) {
    element.style.borderRadius = border_radius + "px"
    element.style.backgroundColor = 'white'
    element.style.color = link_text_color
    element.style.backgroundColor = link_background_color
    element.style.borderColor = link_background_color
    let alpha = parseFloat(link_background_color.split(',')[3])
    if (alpha < 0.25) {
        element.style.borderColor = "#fff"
    }
});
