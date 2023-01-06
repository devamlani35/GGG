from PIL import Image
from google_images_search import GoogleImagesSearch
from io import BytesIO

API_KEY="AIzaSyDFSZYy-9XIndulPn49xhflNBqKLA0bhqY"
cx="16012a884b723458c"
gis = GoogleImagesSearch(API_KEY, cx)

my_bytes_io = BytesIO()
gis.search({'q': 'puppies', 'num': 3})
for image in gis.results():
    my_bytes_io.seek(0)

    # take raw image data
    raw_image_data = image.get_raw_data()

    # this function writes the raw image data to the object
    image.copy_to(my_bytes_io, raw_image_data)

    # or without the raw data which will be automatically taken
    # inside the copy_to() method
    image.copy_to(my_bytes_io)

    # we go back to address 0 again so PIL can read it from start to finish
    my_bytes_io.seek(0)

    # create a temporary image object
    temp_img = Image.open(my_bytes_io)
    
    # show it in the default system photo viewer
    temp_img.show()
