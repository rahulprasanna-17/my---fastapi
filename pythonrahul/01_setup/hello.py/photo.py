# Fix the analytics part of the snaplet ai application

import os
import json
import time
from datetime import datetime
from PIL import Image


class ImageAnalytics:
    """Track and display analytics for image uploads and processing."""
    
    def __init__(self, analytics_file="image_analytics.json"):
        self.analytics_file = analytics_file
        self.uploads = self._load_analytics()
    
    def _load_analytics(self):
        """Load existing analytics from file."""
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_analytics(self):
        """Save analytics to file."""
        with open(self.analytics_file, 'w') as f:
            json.dump(self.uploads, f, indent=2)
    
    def log_upload(self, image_path, processed_path, status="success", error_msg=None):
        """Log an image upload/processing event."""
        upload_record = {
            "timestamp": datetime.now().isoformat(),
            "original_file": os.path.basename(image_path),
            "original_path": image_path,
            "processed_path": processed_path,
            "status": status,
            "error": error_msg,
            "file_size": os.path.getsize(image_path) if os.path.exists(image_path) else 0
        }
        self.uploads.append(upload_record)
        self._save_analytics()
        return upload_record
    
    def get_uploads_list(self):
        """Get formatted list of all uploads."""
        if not self.uploads:
            return "No uploads yet."
        
        output = "\n" + "="*70 + "\n"
        output += "ANALYTICS: Image Uploads List\n"
        output += "="*70 + "\n"
        
        for idx, upload in enumerate(self.uploads, 1):
            output += f"\n[{idx}] {upload['original_file']}\n"
            output += f"    Timestamp: {upload['timestamp']}\n"
            output += f"    Status: {upload['status']}\n"
            output += f"    Size: {upload['file_size']} bytes\n"
            if upload['processed_path']:
                output += f"    Processed: {upload['processed_path']}\n"
            if upload['error']:
                output += f"    Error: {upload['error']}\n"
        
        output += "\n" + "="*70 + "\n"
        output += f"Total Uploads: {len(self.uploads)}\n"
        output += f"Successful: {sum(1 for u in self.uploads if u['status'] == 'success')}\n"
        output += f"Failed: {sum(1 for u in self.uploads if u['status'] == 'failed')}\n"
        output += "="*70 + "\n"
        
        return output


# Global analytics tracker
analytics = ImageAnalytics()


def process_image(image_path):
    """Process an image by resizing it to 800x600 and saving it."""
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            error_msg = f"Image file not found: {image_path}"
            analytics.log_upload(image_path, None, "failed", error_msg)
            raise FileNotFoundError(error_msg)
        
        # Open the image file
        with Image.open(image_path) as img:
            # Perform basic processing (resize to 800x600)
            img = img.resize((800, 600))
            
            # Save the processed image to a new path
            processed_image_path = os.path.splitext(image_path)[0] + "_processed.jpg"
            img.save(processed_image_path)
            
            # Log successful upload to analytics
            analytics.log_upload(image_path, processed_image_path, "success")
            
            print(f"Processed image saved at: {processed_image_path}")
            return processed_image_path
    
    except FileNotFoundError as e:
        print(f"File error: {e}")
        return None
    except Exception as e:
        error_msg = str(e)
        analytics.log_upload(image_path, None, "failed", error_msg)
        print(f"Error processing image: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list-uploads":
            # Display analytics
            print(analytics.get_uploads_list())
        else:
            # Process image
            image_path = sys.argv[1]
            result = process_image(image_path)
            if result:
                print(f"Success: {result}")
                # Display updated analytics
                print(analytics.get_uploads_list())
    else:
        print("Usage:")
        print("  python photo.py <image_path>     - Process an image")
        print("  python photo.py --list-uploads   - Show analytics of all uploads") 

        # fixing the results part of the snaplet ai application

