## Good Enough Practices in Scientific Computing
Wilson et al, 2016, [PLOS](https://arxiv.org/pdf/1609.00037.pdf)

#### Data management
- Save the raw data
- Create the data you wish to see in the world
- Create analysis-friendly data
- Record all the steps used to process the data
- Anticipate the need to use multiple tables
- Submit data to a reputable DOI-issuing repository so that others can access and cite it

#### Software
- Place a brief explanatory comment at the start of every program
- Decompose programs into functions
- Be ruthless about eliminating duplication
- Give functions and variables meaningful names
- Make dependencies an drequirements explicit
- Do not comment and uncomment sections of code to control a program's behavior
- Provide a simple example or test data set
- Submit code to a reputable DOI-issuing repository

#### Collaboration
- Create an overview of your project
- Create a shared public "to-do" list
- Make the license explicit
- Make the project citable

#### Project organization
- Put each project in its own directory, which is named after the project
- Put text documents associated with the project in the ``doc`` directory
- Put raw data and metadata in a ``data`` directory
- Put project source code in the ``src`` directory
- Put external scripts, or compiled programs in the ``bin`` directory
- Name all files to reflect their content or function

#### Keep track of changes
- Back up (almost) everything created by a human being as soon as it is created
- Keep changes small
- Share changes frequently
- Create, maintain, and use a checklist for saving and sharing changes to the project
- Store each project in a folder that is mirroried off the researcher's working machine

#### Manuscripts
- Either single master copy with rich text like Google Doc, or text-based doc under version control in LaTeX or Markdown, etc
