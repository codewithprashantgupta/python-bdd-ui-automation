# Python-BDD-UI-Automation

This repository provides a generic framework for implementing UI test automation using Python and BDD (Behavior-Driven Development).



## Features
- **Behavior-Driven Development**: Write test cases in Gherkin syntax for better readability and collaboration.
- **Reusable Components**: Easily configurable for various test scenarios.
- **Seamless Integration**: Compatible with CI/CD pipelines.


## Getting Started

Follow the steps below to set up the framework and run your tests.

### Prerequisites:
- Python 3.x installed on your system.
- `pip` (Python package manager) available.
- A terminal/command prompt with `git` installed.

####  1. Clone this repository and navigate to the project directory:
```bash
   git clone <repository-url>
```

####  2. Create and activate a virtual environment:
```bash
    python3 -m venv venv-bdd
    cd venv-bdd/bin/
    . ./activate
```

####  3. Install the required dependencies:
```bash
    cd python-bdd/
    pip install -r requirements.txt
```



## Run Tests

#### Basic Test Execution
```bash
behave -Dstage=test
```

#### Run Specific Feature File
```bash
behave -Dstage=test features/<file_name.feature>
```

#### Run Tests with Tags
```bash
behave -Dstage=test --@tags=<tag-id> features/<file_name.feature> 
```

#### Enable Detailed Logging
```bash
behave -Dstage=test --@tags=<tag-id> --logging-level=info feature/<file_name.feature> 
```


## Framework Overview
The folder structure of this framework is as follows:


```bash
python-bdd/
│
├── features/
│   ├── steps/           # Step definition files
│   ├── environment.py   # Hooks for test setup and teardown
│   ├── <feature files>  # Gherkin scenarios
|   ├── config.ini       # Configurations file (updated by secret mgmt.)
|   ├── .config.ini      # Hidden configurations file (local file)
│
├── pages/               # Page locators
├── utils/               # Utility functions for test interactions
├── reports/             # Generated test reports
├── screenshots/         # Captured screenshots
└── README.md            # Project documentation

```


## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the framework.


## License
This project is licensed under the MIT License.