# StockWize
Stock Management Application for CSI4999


Steps for setting up stockwize 

Step 1) Download miniconda

https://docs.anaconda.com/miniconda/

Step 2) Create Virtual Enviroment

   1) open terminal
      
   2) conda create --name myenv python=3.12 # note myenv can be whatever you want
      
   3) conda activate myenv # activates virtual env

Step 3) Configure python interpreter 

  1) If on pycharm community edition
     a) Settings
     
     b) Python Interpreter
     
     c) add interpreter
     
     d) add local interpreter
     
     e) conda enviroment
     
     f) use existing enviroment
     
     g) If the conda executable field: go to your conda.exe file should be something like this
       
      /Users/bende/miniconda3/condabin/conda
     
     h) use existing enviroment: name of your virutal enviroment and then click ok
     
     i) you should see your enviroment name in the lower right hand corner
     
     j) open terminal in pycharm
     
     k) conda activate yourenviromentname
     
     l) pip install -r requirements.txt

  3) If on VSCode
     make sure python extension is downloaded before you do anything
     
     a) Ctrl + Shift + P on windows or Cmd + Shift + P on mac
     
     b) type in Select Interpreter and hit enter
     
     c) select your virtual enviroment you made
     
     d) open a terminal
     
     e) type in conda activate yourenviroment name
     
     f) pip install -r requirements.txt

Steps for setting up frontend

   1) Ensure you have node installed. Download instructions [here](https://nodejs.org/en/download/package-manager).

   2) Navigate to the root directory of the project, and run `npm install` (Only need to do this once)
   
   3) `npm run dev` To start the servr

   4) Go to http://localhost:3000. All of the frontend code is in the /app directory (Unfortunately it can't be renamed). Any changes made to the code should be recompiled automatically, and can be viewed by refreshing the browser. This project has been set up with the following specs: Next.JS framework (React with some convenience tooling) Typescript, ESLint, and App Router. 

   5) Learn more about Next/React [here](https://nextjs.org/docs/getting-started/project-structure)
