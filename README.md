# Stargazing_Planner
End of Foundations year project  





https://github.com/Nyaguthii-C/Stargazing_Planner/assets/111014832/0b081865-815b-42bd-9eec-c591491e334f



## Introduction

Stargazing Planner is a web application developed with the Flask framework.  
Its primary objective is to be a tool that demystifies celestial observations, catering to both novice stargazers and amateur astronomers.  
To achieves this, it leverages location data and user preferences. Users input their whereabouts and select celestial objects of interest.  
Subsequently, the app delivers two vital pieces of information. Firstly, it discerns which celestial objects are visible from the user's precise location. Secondly, it furnishes precise sky coordinates, guiding users to the exact celestial coordinates.  


## Installation

To install the web application,  
### 1. Clone the  repository  

    git clone https://github.com/Nyaguthii-C/Stargazing_Planner.git

### 2. Setting Up a Virtual Environment     
  It's recommended to use a virtual environment to manage dependencies for this project. Here's how to set it up:
-  **Open a terminal or command prompt.**  

-  **Navigate to your project directory:**  
   ```bash
   cd /path/to/your/project

-  **Set Up Virtual Environment** 
   ```bash
   python -m venv venv

### 3. Activate the virtual environment:  
- **On windows**  
    ```bash
    venv\Scripts\activate  

 - **macOS and Linux:**
    ```bash
    source venv/bin/activate

### 4. Installing Dependencies 
Once the virtual environment is activated, you can install the required dependencies from the requirements.txt file:
    ```bash
    pip install -r requirements.txt

### 5. Additional Configuration  
Since Stargazing Planner utilizes [Astronomy API](https://astronomyapi.com/), create an account with Astronomy API and proceed to acquire your Application ID and Aplication Secret. [See here](https://docs.astronomyapi.com/) for more direction.  
Once you have your [Astronomy API](https://astronomyapi.com/) credentials and yout YourAuthString, set a global variable for the authoriazation string to be used in making requests to.  
To set the global variable,  
- **On Linux/macOS:**
    ```bash
    export authorization_string="YourAuthString"
 **Note**
   This commands will set the environment variables for the current session.   
   To make it persistent across sessions, you can **add it to your shell's profile file (e.g., ~/.bashrc, ~/.bash_profile, or ~/.zshrc).**    
- **On Windows**
    ```bash
    set authorization_string="YourAuthString"
**Note**
   This commands will set the environment variables for the current session.   
   To make it persistent across sessions, you can set them in the system environment variables. Here's how:    
  - Search for "Environment Variables" in the Windows Start menu.  
  - Click on "Edit the system environment variables."  
  - In the "System Properties" window, click the "Environment Variables" button.  
  - Under "User variables" or "System variables," click "New" to add a new variable and set its name and value.  



## Usage

1. **Running the Application**
To run the application, run:
    ```bash
    python planner.py

2. **Accessing the Web Application**  
To access the web aplication in your browser, navigate to either of the routes:
    ```bash
     http://127.0.0.1:5000/
     http://localhost:5000/
If running Stargazing Planner inside a container in your local machine, replace *localhost* with  *<container_ip>*  

3. **Stopping the Application**   
To stop the application,
    ```bash
    Ctrl +  C

Happy stargazing!

## Contributing  
-  **Creating an Issue**  
   Create an issue to:
    -  Report a bug.
    -  Suggest an enhancement or new feature.
    -  Discuss major changes or improvements before starting to work on them.  

- **Submitting a Pull Request (PR)**  
To contribute to Stargazing Planner:
    - Fork the [Stargazing Planner repo](https://github.com/Nyaguthii-C/Stargazing_Planner.git)
    - Create a new branch for your changes.
    - Make the necessary code changes.
    - Push the changes to your forked repository.
    - Create a PR from your forked repository to the main repository.


## License

This project is licensed under the **MIT** License - see the [LICENSE](https://github.com/Nyaguthii-C/Stargazing_Planner/blob/main/LICENSE) file for details.







## Acknowledgement  
We would like to acknowledge the following APIs that have been instrumental in the development of our Flask web application:
-  [Astronomy API](https://astronomyapi.com/) - provided astronomical data about stars, planets, and other celestial objects.
- [Sunset and sunrise times API](https://sunrise-sunset.org/api)- provided sunset, sunrise, twilight begin and end times for a given latitude and longitude.
- [pyAstronomy](https://pyastronomy.readthedocs.io/en/latest/index.html) - provided a function that was used in the convertion of celestial coordinates into local horizon coordinates (ALT/AZ).
