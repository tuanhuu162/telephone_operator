# telephone_operator
Repo for the telephone operator project

## How to run
1. Clone the repo
2. Install virtualenv with command `pip install virtualenv` and then create a virtual environment with command `virtualenv venv` for python version > 3.11 
3. Activate the virtual environment with command `source venv/bin/activate`
4. Install poetry with command `pip install poetry`
5. Install dependencies with command `poetry install`
6. Run the project with command `python main.py`
    Sample command :
    `python main.py --list_operator_files sample_data/operator/operatorA sample_data/operator/operatorB --phone_number_file sample_data/telephone --output_file output.txt`
    `python main.py -l sample_data/operator/operatorA sample_data/operator/operatorB -p sample_data/telephone`
    
## How to run tests
1. Run the project with command `python -m unittest`
