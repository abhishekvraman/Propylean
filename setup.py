from distutils.core import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  name = 'Propylean',       
  packages = ['Propylean'],   # Chose the same as "name"
  version = '00.00.03',      
  license='MIT',       
  description = 'The open-source analytics package for chemical process industries.', 
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'ABHISHEK V RAMAN',                
  author_email = '',      
  url = 'https://github.com/abhishekvraman/Propylean',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['chemical', 'manufacturing', 'hydraulics', 'steady-state', 'process-flow-diagram', 
              'line-sizing', 'control-valves', 'pump-sizing', 'vessel-sizing'],   # Keywords that define your package best
  install_requires=[            
          'thermo',
          'fluids',
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Manufacturing',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Chemistry',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10',
  ],
)