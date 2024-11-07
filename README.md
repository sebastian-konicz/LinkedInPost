# LinkedIn Post Automation Project
This project automates the process of posting on LinkedIn using the LinkedIn API and integrates with OpenAI's API to generate content. The project is designed to streamline LinkedIn posting by fetching article data, creating posts with images, and publishing them.
![Logo projektu](src/project_logo.png)

## Features
- **Automated LinkedIn Posts**: Automatically post on LinkedIn with generated or fetched content.
- **Content Generation**: Integrates with OpenAI API for generating text and images.
- **Data Management**: Organizes and stores data in `src/data` for easy access and management.
- **Customizable**: Easily configurable with a `.env` file for sensitive information.

## Project Structure
- `.github/workflows`: GitHub Actions workflows for CI/CD.
- `config`: Configuration files, including settings for APIs.
- `src`: Contains main modules for data scraping, API interaction, and posting automation.
  - `linkedin_client.py`: Handles LinkedIn API interactions.
  - `medium_scraper.py`: Scrapes top article in AI subject on a given day form medium.com
  - `openai_api.py` & `openai_api_images.py`: Interact with OpenAI API for text and image generation.
- `venv`: Virtual environment directory (not included in the repository).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/LinkedInPost.git
   ```
2. Navigate to the project directory:
   ```bash
   cd LinkedInPost
   ```
3. Install dependencies:
   ```bash
   cd LinkedInPost
   ```
4. Configure your .env file with API keys and other sensitive data.

## Usage
Run the main script to post on LinkedIn:
   ```bash
      python src/main.py
   ```

## Configuration
Ensure the following variables are set in your .env file:

- `LINKEDIN_CLIENT_ID`: Your LinkedIn client id.
- `LINKEDIN_CLIENT_SECRET`: Your LinkedIn primary client secret.
- `LINKEDIN_ACCESS_TOKEN`: Your LinkedIn access token.
- `OPENAI_API_KEY`: Your OpenAI API key.

## License
This project is licensed under the MIT License. See LICENSE for more details.