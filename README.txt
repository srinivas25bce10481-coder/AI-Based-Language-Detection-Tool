BYOP: AI Language Detection System
Author: Srinivas.S.S
Registration No: 25BCE10481
Project Category: Natural Language Processing (NLP)

Project Overview
The AI Language Detection System is a high-performance Command Line Interface
(CLI) application developed to identify the linguistic origin of digital text. By implementing advanced statistical probability models, the system evaluates input—ranging
from single phrases to comprehensive text files—to determine the most probable language, providing a transparent breakdown of its analytical confidence.

Core Features
• Real-time Analysis: Instantaneous detection of manually entered text strings.
• File System Integration: Support for batch processing and auditing of .txt
documents.
• Probability Distribution: Displays the primary language match alongside
three alternative candidates with precise percentage-based confidence scores.
• Validation Logic: Automated warnings for insufficient data lengths to ensure
result integrity.
• Data Persistence: Integrated history logging that tracks the last 10 operations
via a history.json architecture.

Getting Started
Technical Requirements
This system requires a stable installation of Python 3.x.

Installation Procedure
1. Download or clone the project repository to your local machine.
2. Install the necessary dependency using the following command:


pip install langdetect

Application Execution
To initialize the system, navigate to the project directory and execute:
python main.py

Operation Instructions
Upon initialization, the system presents a formal management menu:
• Analyze text input: Used for direct manual entry and testing.
• Analyze a .txt file: Used for processing external file paths.
• View analysis history: Accesses the local data log for previous sessions.
• Exit: Terminates the application and saves the current state.

Methodology Note
The engine utilizes N-gram frequency analysis coupled with a Naive Bayes Classifier. It references pre-trained language profiles to match linguistic patterns. For
consistency in academic testing, a deterministic seed is utilized within the detection
factory to ensure reproducible results.



