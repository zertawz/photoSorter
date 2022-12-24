import os
import exifread
from shutil import copy2

def sort_photos(source_dir, target_dir):
  # Create a dictionary to store the sorted photos
  sorted_photos = {}

  # Iterate through the files in the source directory
  for file in os.listdir(source_dir):
    # Check if the file is a photo (assuming it has a .jpg or .jpeg extension)
    if file.endswith('.jpg') or file.endswith('.jpeg'):
      # Open the photo file
      with open(os.path.join(source_dir, file), 'rb') as f:
        # Read the EXIF metadata
        tags = exifread.process_file(f)
        # Get the date the photo was taken
        date_taken = tags.get('EXIF DateTimeOriginal', None)
        # If the date is available, add the photo to the dictionary using the date as the key
        if date_taken:
          if date_taken not in sorted_photos:
            sorted_photos[date_taken] = []
          sorted_photos[date_taken].append(file)

  # Iterate through the sorted photos
  for date, photos in sorted_photos.items():
    # Create a directory for the photos with this date (if it doesn't already exist)
    date_dir = os.path.join(target_dir, date)
    if not os.path.exists(date_dir):
      os.makedirs(date_dir)
    # Move each photo to the target directory and rename it with the date
    for photo in photos:
      copy2(os.path.join(source_dir, photo), date_dir)
      os.rename(os.path.join(date_dir, photo), os.path.join(date_dir, f'{date}_{photo}'))

#Example usage:
#sort_photos('/path/to/source/directory', '/path/to/target/directory')
