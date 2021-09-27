from django.conf import settings
import os


# def writecss(username, color1, color2, body_font_color, primary_font_size, name_font_size,
#              border_radius, link_text_color, link_background_color, font, use_background_image,
#              brightness_css_factor, desktopimage, mobileimage):
def writecss(user):
  color1 = user.preferences.color1
  color2 = user.preferences.color2
  body_font_color = user.preferences.body_font_color
  font = user.preferences.font_family
  use_background_image = user.preferences.use_background_image
  mobileimage = user.preferences.background_image_mobile.url
  desktopimage = user.preferences.background_image_desktop.url
  background_image_brightness = user.preferences.background_image_brightness
  brightness_css_factor = background_image_brightness / 100
  primary_font_size = user.preferences.primary_font_size
  name_font_size = user.preferences.name_font_size
  border_radius = user.preferences.border_radius
  link_background_color = user.preferences.link_background_color
  link_border_color = user.preferences.link_border_color
  link_text_color = user.preferences.link_text_color
  font_family = user.preferences.font_family

  css = f"""

@font-face {{
    font-family: 'customfont';
    src:  url("/media/fonts/{font}")
}}

body {{
  margin: 0;
  padding: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  background-image: linear-gradient(90deg, {color1}, {color2});
  min-height: 100vh;
  color: {str(body_font_color)};
  font-family: 'customfont', sans-serif;
  font-size: {str(primary_font_size)};
}}

/*TODO - Style Overflow*/
.overflow {{
  padding: 10px;
  max-width: 640px;
  margin: 0 auto;
  margin-bottom: 100px;
}}

.bio {{
  text-align: center;
  margin-bottom: 20px;
}}

a {{
  color: white;
  text-decoration: none;
}}

a:hover {{
  color: #eecda3;
}}

.skip {{
  font-size: 30px;
  padding: 5px;
}}

.skip i {{
  color: white;
}}

.toinvisible {{
  opacity: 0;
}}

.hidden {{
  background: transparent;
  border: none;
}}

.skip i:hover {{
  color: #fff;
}}

.skip-text {{
  font-size: 0.8rem;
}}

.content {{
  overflow-y: auto;
  max-height: 100vh;
}}

.formcontainer {{
  max-width: 760px;
  margin: 0 auto;
}}

.subcontent {{
  max-width: 75%;
  margin: 0 auto;
}}

.image-border {{
  padding: 0;
  background-image: transparent;
  height: 105px;
  width: 105px;
  border-radius: 50%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
}}

.round {{
  height: 100px;
  width: 100px;
  border-radius: 50%;
  /*border: 1px solid white;*/
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}}

.center {{
  text-align: center;
}}

.name {{
  font-size: {name_font_size}px;
}}

.cta {{
  border-radius: 50px;
  padding-right: 50px;
  padding-left: 50px;
  padding-top: 15px;
  padding-bottom: 15px;
  font-weight: bold;
  margin-bottom: 100px;
}}

.cta1 {{
  border: solid 2px white;
  color: black;
  background: white;
}}

.cta1:hover {{
  background:  transparent;
  transition: 0.3s;
}}

.form-group input {{
  border: 1px solid rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.85);
  border-radius: 50px;
  padding: 25px;
}}

#copyinput, #copyinput2 {{
  border: 1px solid rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50px;
  padding: 25px;
  opacity: 1;
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
}}

.copy {{
  background: transparent;
  border: none;
  outline: none;
  color: {body_font_color};
}}


@media only screen and (max-width: 800px) {{
  .content, .formcontainer {{
    max-width: 98%;
  }}
}}


.page-link {{
  border: 1px solid {link_border_color};
  border-radius: {str(border_radius)}px;
  padding: 20px;
  text-align: center;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: {link_text_color};
  background-color: {link_background_color};
}}

.page-link:hover {{
  background: transparent;
  background-position: center;
  background-repeat: no-repeat;
}}

.page-link .fa-pencil-alt, .page-link .linkviews {{
  position: absolute;
  right: 30px;
}}

.page-link .fa-grip-lines {{
  position: absolute;
  left: 30px;
  font-size: 0.75rem;
  height: 100%;
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  left: 0;
}}

#linkicon {{
  position: absolute;
  right: 10%;
}}


.socials {{
  width: 50%;
  margin: 25px auto;
  font-size: 32px;
  text-align: center;
  margin-bottom: 50px;
}}

.edit {{
  display: block;
}}

.space-between {{
  display: flex;
  justify-content: space-between;
}}






.footer {{
    width: 100vw;
    position: absolute;
    position: fixed;
    bottom: 0;
    left: 0;
    background: rgba(255, 255, 255, 1);
    text-align: center;
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 65px;
    padding: 10px;
    display: flex;
    z-index: 1000;
    box-shadow: 1px 1px 1px 1px grey;
}}

.footer img {{
    height: 24px;
    width: 24px;
    margin: 0;
    transition: all 0.4s;
}}

.footer img:hover {{
    height: 48px;
    width: 48px;
}}

.footer-active {{
}}

@media only screen and (min-width: 800px) {{
  .footer {{
    top: 0;
    height: 100vh;
    width: 65px;
    flex-direction: column;
  }}
}}


.previewlinkedit {{
  overflow-y: auto;
}}

.previewlinkedit a {{
  color: {body_font_color};
  text-decoration: underline;
}}

input[type="checkbox"] {{
margin: 0;
padding: 0;
  position: relative;
  width: 80px;
  height: 40px;
  -webkit-appearance: none;
  background: #c6c6c6;
  outline: none;
  border-radius: 50px;
  transition: .5s;

}}

input:checked[type="checkbox"] {{
  background: #03a9f4;
}}

input[type="checkbox"]:before {{
  content: '';
  position: absolute;
  width: 40px;
  height: 40px;
  border-radius: 50px;
  top: 0;
  left: 0;
  background: #fff;
  box-shadow: 0 2px 5px rgba(0,0,0, .2);
  transition: .5s;
}}

input:checked[type="checkbox"]:before {{
  left:40px;
}}

.thankyou {{
  text-align: center;
}}

textarea#id_call_to_action {{
  border: 1px solid rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.85);
  border-radius: 25px;
}}

"""

  if use_background_image == 'true':
    css += f"""
  body {{
      color: #fff;
      background-image: linear-gradient(90deg, rgba(0,0,0,{brightness_css_factor}), rgba(0,0,0,{brightness_css_factor}) ), url({desktopimage});
  }}
  @media only screen and (max-width: 800px) {{
    body {{
      background-image: linear-gradient(90deg, rgba(0,0,0,{brightness_css_factor}), rgba(0,0,0,{brightness_css_factor}) ), url({mobileimage});
    }}
  }}
  """

  if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, f'customstylesheets')):
    os.mkdir(os.path.join(settings.MEDIA_ROOT, f'customstylesheets'))

  PATH = os.path.join(
      settings.MEDIA_ROOT, f'customstylesheets/{user.username}.css')

  with open(PATH, 'w') as f:
    f.write(css)

  return 'Css Written'
