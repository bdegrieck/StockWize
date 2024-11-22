# StockWize

Stock Management Application for CSI4999

## One Time Setup for Backend

The following assumes you have an up to date version of python installed, as well as the appropriate IDE for the different setup options.

### Option 1. Miniconda/Pycharm

- [Download miniconda](https://docs.anaconda.com/miniconda/)
- Create Virtual Enviroment

   1. Open terminal
   2. `conda create --name myenv python=3.12 # "myenv" can be whatever you want` 
   3. `conda activate myenv # activates virtual env`

- Configure python interpreter 

  1. If on pycharm community edition, go to `Settings> Python Interpreter> Add interpreter> Add Local Interpreter> Conda Enviroment > Use Existing Enviroment`. Your conda.exe file should be something like `/Users/username/miniconda3/condabin/conda`

  2. `Use existing enviroment` - name of your virutal enviroment and then click `Ok`
  3. You should see your environment name in the lower right hand corner
  4. Open terminal in pycharm
  5. `conda activate yourenviromentname` and `pip install -r requirements.txt`
    
### Option 2. Miniconda/VSCode

   1. Install the VSCode Python Extension
     
   2. `Ctrl + Shift + P` on Windows or `Cmd + Shift + P` on Mac, type `Select Interpreter` and press Enter
   
   3. Select your virtual environment you made
     
   4. Open a terminal and run `conda activate yourenviromentname` and `pip install -r requirements.txt`

### Option 3. Terminal Only

   1. Create a virtual environment with `py -m venv yourenvironmentname`

   2. Activate the environment with `.\yourenvironmentname\Scripts\activate` on Windows or `source yourenvname/bin/activate` on Mac/Linux

   3. Install dependencies with `pip install -r requirements.txt`

## Onetime Setup for Frontend

   - Navigate to the root directory of the project, and run `npm install`.

## Running the App

   1. Activate your python virtual environment with the appropriate method for your setup
   2. Ensure you are in the root directory of the project in the terminal and run `npm start`

## Gotchas / Common Issues

   1. If some resources are failing to load, and the developer console gives an error along the lines of 

   ```
      Cross-Origin Request Blocked: The Same Origin Policy disallows
   reading the remote resource at https://some-url-here. (Reason:
   additional information here).
   ```

   Try restarting your computer and rerunning the project.
   