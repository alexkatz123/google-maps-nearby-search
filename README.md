
# Activity Finder

This Python script allows you to find places for a specific activity within a 2-hour drive from a given location using the Google Maps API. It retrieves details such as name, address, travel time, contact number, website, and contact email of the places and saves them into a CSV file named after the activity type.

## Features

- Converts postcodes, addresses, or coordinates into latitude and longitude.
- Finds places within a specified radius and retrieves their details.
- Calculates travel time to each place and filters places within a 2-hour drive.
- Extracts contact email addresses from business websites (if available).
- Saves the results into a CSV file named after the specified activity type.

## Requirements

- Python 3.6+
- Google Maps API Key

## Installation

1. Clone the repository or download the script files.

2. Navigate to the project directory.

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Getting the API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Navigate to the **API & Services** section and click on **Credentials**.
4. Click on **Create Credentials** and select **API key**.
5. Copy the generated API key.

## Enabling Necessary APIs

Ensure the following APIs are enabled for your project in the Google Cloud Console:

- Geocoding API
- Maps JavaScript API
- Places API
- Distance Matrix API

To enable these APIs:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project.
3. Navigate to **API & Services** > **Library**.
4. Search for each API and click on **Enable**.

## Billing Information

A billing account is required for the Google Maps API to work. Make sure you have a billing account set up and linked to your project. You can set up billing in the [Google Cloud Console](https://console.cloud.google.com/billing/).

## Usage

1. Open the \`app.py\` file and replace \`YOUR_GOOGLE_MAPS_API_KEY\` with your actual Google Maps API key.

2. Run the script:
   ```bash
   python app.py
   ```

3. Follow the prompts to enter your starting location, search center location, and activity type.

4. The script will process the information and save the results to a CSV file named after the specified activity type (e.g., \`swimming.csv\`).

## Example

```
Enter your starting location (latitude,longitude or DMS format or postcode): 52°37'17.0"N 2°14'41.6"W
Enter the search center location (latitude,longitude or DMS format or postcode): 52°37'17.0"N 2°14'41.6"W
Enter the activity type (e.g., swimming): swimming
```

After running the script, a file named \`swimming.csv\` will be created with the details of the places found.

## Notes

- Make sure your Google Maps API key has the necessary permissions and billing enabled.
- The script uses web scraping to extract contact emails, which might not always be accurate or available.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
