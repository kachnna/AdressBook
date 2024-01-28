## Setup INSTRUCTION "Alfred" 

## 1) Setup by pipenv

1. **Clone this respository into a folder by command:**
   ```
   git clone https://github.com/kachnna/AdressBook.git
   ```
2. **Install pipenv:**
   ```
   pip install pipenv
   ```
3. **Setup the application:**
   ```
   cd al_addressbook
   ```
   ```
   pipenv install --deploy
   ```
4. **Run the pipenv:**
   ```
   pipenv shell
   ```
5. **Run "Alfred":**
   ```
   pipenv run python book/main.py
   ```
## 2) Setup by docker

1. **Create an image:**
  ```
  docker build . -t [your profile name in docke hub]/[image name]
  ```

2. **Spin up a new container:**
  ```
  docker run -it -t [your profile name in docke hub]/[image name]
  ```
   
