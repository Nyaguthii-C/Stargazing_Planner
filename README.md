# Stargazing_Planner
End of Foundations year project  

## Introduction
Stargazing Planner is a web application developed with the Flask framework.  
Its primary objective is to be a tool that demystifies celestial observations, catering to both novice stargazers and amateur astronomers.  
To achieves this, it leverages location data and user preferences. Users input their whereabouts and select celestial objects of interest.  
Subsequently, the app delivers two vital pieces of information. Firstly, it discerns which celestial objects are visible from the user's precise location. Secondly, it furnishes precise sky coordinates, guiding users to the exact celestial coordinates.  
It utilizes data and methods from [Astronomy API](https://astronomyapi.com/), [Sunset and sunrise times API](https://sunrise-sunset.org/api) and [pyAstronomy](https://pyastronomy.readthedocs.io/en/latest/index.html),a collection of astronomy related packages.  
- **NOTE:** To retrieve the correct ephemeris data from the Stargazing Planner, ensure to enter the correct latitude and longitude for your location.
Entering incorrect or invalid coordinates values will return incorrect ephemeris data.


## Installation
To install the web application,  
1. ### Clone the  repository  
    - **git clone https://github.com/Nyaguthii-C/Stargazing_Planner.git**
2. ### Setting Up a Virtual Environment  
  It's recommended to use a virtual environment to manage dependencies for this project. Here's how to set it up:
1. **Open a terminal or command prompt.**  

2. **Navigate to your project directory:**  
   ```bash
   cd /path/to/your/project

3. **Set Up Virtual Environment** 
   ```bash
   python -m venv venv

4. **Activate the virtual environment:**  
- **On windows**  
    ```bash
    venv\Scripts\activate  

 - **macOS and Linux:**
    ```bash
    source venv/bin/activate

5. **Installing Dependencies**  
Once the virtual environment is activated, you can install the required dependencies from the requirements.txt file:
    ```bash
    pip install -r requirements.txt







## Usage

## Contributing


## Licensing








