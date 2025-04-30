import os
import urllib.request

def download_sample_images():
    """Download sample black and white images for testing."""
    # Create directory for sample images
    os.makedirs('static/samples', exist_ok=True)
    
    # URLs of some sample black and white images (public domain or creative commons)
    sample_images = [
        {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/b/b3/Vintage_London_taxi.jpg',
            'filename': 'vintage_london_taxi.jpg'
        },
        {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/5/5e/Ellis_Island_arrivals.jpg',
            'filename': 'ellis_island_arrivals.jpg'
        },
        {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/9/90/Spital_Square_London.jpg',
            'filename': 'spital_square_london.jpg'
        }
    ]
    
    # Download each sample image
    for img in sample_images:
        output_path = os.path.join('static/samples', img['filename'])
        if not os.path.exists(output_path):
            print(f"Downloading {img['filename']}...")
            urllib.request.urlretrieve(img['url'], output_path)
            print(f"Downloaded {img['filename']}")
        else:
            print(f"{img['filename']} already exists")

if __name__ == "__main__":
    download_sample_images()