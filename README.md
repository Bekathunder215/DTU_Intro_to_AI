# DTU Introduction to Artificial Intelligence Projects

Welcome to the repository for DTU's Human-Centered Artificial Intelligence: Introduction to AI course projects. This collection showcases various projects and assignments developed during the course, focusing on foundational AI concepts and techniques.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository contains projects undertaken as part of the Introduction to Artificial Intelligence course at the Technical University of Denmark (DTU). The course covers essential AI topics, including:

- **Search Algorithms**: Implementing uninformed and informed search techniques to solve AI problems.
- **Adversarial Search**: Applying adversarial search techniques for AI in games.
- **Knowledge Representation**: Utilizing logical techniques for the representation of knowledge and reasoning.
- **Machine Learning**: Exploring foundational concepts in machine learning and their applications.

For detailed course objectives and curriculum, refer to DTU's official curriculum for Human-Centered Artificial Intelligence. ([dtu.dk](https://www.dtu.dk/english/education/graduate/msc-programmes/human-centered-artificial-intelligence/curriculum?utm_source=chatgpt.com))

## Project Structure

The repository is organized as follows:

- **`game.py`**: Contains the implementation of the game logic, including the `Game` class responsible for managing the game state, scoring, and moves.
- **`ai.py`**: Implements the AI agent, featuring the `AI` class that utilizes techniques like Minimax search with alpha-beta pruning to determine optimal moves.
- **`ui.py`**: Manages the user interface, facilitating interaction between the user and the game.
- **`constants.py`**: Defines global constants used throughout the project, such as grid size and tile spawn probabilities.
- **`main.py`**: The main entry point of the application, orchestrating the game flow and integrating various components.
- **`requirements.txt`**: Lists the Python dependencies required to run the projects.

## Installation

To set up the projects locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Bekathunder215/DTU_Intro_to_AI.git
   cd DTU_Intro_to_AI

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt

## Usage

To run the main application:
  ```bash
  python main.py
  ```

This command launches the game interface, allowing you to interact with the AI-driven game. For detailed examples and usage instructions, refer to the documentation within each module.


## Contributing

Contributions to enhance the projects are welcome. To contribute:

1. Fork the repository.
2. Create a new branch:
  ```bash
  git checkout -b feature/YourFeatureName
  ```
3. Commit your changes:
  ```bash
  git commit -m 'Add some feature'
  ```
4. Push to the branch:
  ```bash
  git push origin feature/YourFeatureName
  ```
5. Open a pull request detailing your changes.


## License

This repository is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

*Note: This README template is inspired by best practices in README documentation, including examples from the [Best-README-Template](https://github.com/othneildrew/Best-README-Template) and other notable repositories.*
