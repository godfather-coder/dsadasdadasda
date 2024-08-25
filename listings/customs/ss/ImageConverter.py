import base64
import requests

class ImageConverter:
    def __init__(self, image_urls):
        self.image_urls = image_urls

    def _download_image(self, image_url):
        """Download an image from a given URL."""
        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve image from {image_url}. Status code:", response.status_code)
            return None

    def _to_base64(self, image_content):
        """Convert image content to base64 format."""
        if image_content:
            return base64.b64encode(image_content).decode('utf-8')
        return None

    def get_base64_images(self):
        base64_images = []
        for url in self.image_urls:
            image_content = self._download_image(url)
            base64_image = self._to_base64(image_content)
            if base64_image:
                base64_images.append(base64_image)
        return base64_images
