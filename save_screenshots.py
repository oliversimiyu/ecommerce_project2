import os
import base64
from PIL import Image
import io

def save_image(image_data, filename):
    # Convert base64 to image and save
    img = Image.open(io.BytesIO(base64.b64decode(image_data)))
    img.save(filename)

# Create screenshots directory if it doesn't exist
os.makedirs('screenshots', exist_ok=True)

# Save the screenshots
save_image(login_image_data, 'screenshots/login.png')
save_image(register_image_data, 'screenshots/register.png')
save_image(products_image_data, 'screenshots/products.png')
save_image(product_detail_image_data, 'screenshots/product-detail.png')
save_image(cart_image_data, 'screenshots/cart.png')
save_image(checkout_image_data, 'screenshots/checkout.png')
