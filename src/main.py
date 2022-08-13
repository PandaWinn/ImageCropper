from PIL import Image
import streamlit as st
from time import sleep
import zipfile
from io import BytesIO


def get_image_params(image):
    with Image.open(image) as im:
        global im_name
        sizes = im.getbbox()
        original_width = sizes[2]
        original_height = sizes[3]
        im_name = image.name.split('.')[0]
        st.write(im_name)
    return original_width, original_height
    
    
def crop_images(image, original_width, original_height, width, height):
    n_pictures = int(original_width/width)
    st.write(f'You\'ll have {n_pictures} images after cropping')
    list_images=[]
    
    for i in range(int(n_pictures)):
        with Image.open(image) as im:

            # The crop method from the Image module takes four coordinates as input.
            # The right can also be represented as (left+width)
            # and lower can be represented as (upper+height).
            (left, upper, right, lower) = ((i*width), 0, (i*width+width), 1080)
            progress = round(50/n_pictures)
            bar.progress(50+i*progress)

            # Here the image "im" is cropped and assigned to new variable im_crop
            im_crop = im.crop((left, upper, right, lower))
            st.image(im_crop)
            name = im_name + str(i) + '.png'
            list_images.append(im_crop)
    return list_images

                
            
#GUI WITH STREAMLIT

st.markdown('# Image Cropper App **- Lucas v1.0**')
st.text('1 - Select your image \n2 - Adjust the parameters for the final images \n3 - Press the crop button')
st.markdown('#')
bar = st.progress(0)
t = st.empty()
uploaded_image = st.file_uploader("Choose an image to be cropped")
st.sidebar.header('Select the parameters for the final image')
st.markdown('#')
st.subheader('To clear memory, click below')
clear_button = st.button("Clear All")


#sidebar for user to pick width of his final images
with st.sidebar.form(key='param_select'):
    width = st.number_input(label='Width', value=1080)
    height = st.number_input(label='Heigth (not currently in use)', value=1080)
    crop_button = st.form_submit_button(label='Crop!')
    
with st.sidebar.form(key='debug'):
    magic_but = st.form_submit_button(label='Magic')
    
with st.spinner('Code is running'):
    if crop_button:
        original_width, original_height = get_image_params(uploaded_image)
        bar.progress(50)
        st.write('Cropped images shown below')
        list_images = crop_images(uploaded_image, original_width, original_height, width, height)
        for item in list_images:
            st.write(item)
        bar.progress(100)
        st.success('Pictures cropped successfully!')
        
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipF:
            i=0
            for file in list_images:
                i=i+1
                img_byte_arr = BytesIO()
                file.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                zipF.writestr('cropped'+str(i)+'.png', img_byte_arr , compress_type=None)
            zipF.close()
        
        zipfile_ob = zip_buffer.getvalue()
        btn = st.download_button(
            label = 'Download',
            data = zipfile_ob,
            file_name = 'cropped3.zip',
            mime = 'application/zip'
        )
        st.experimental_memo.clear()
if magic_but:
    st.snow()
