# PharmaQ
А platform, that connects patients with certified pharmacists, allowing patients to ask health-related questions and receive reliable answers.

# PharmaQ

This guide will walk you through setting up the **PharmaQ** application using Docker.

---

## Prerequisites

Make sure you have the following tools installed on your system:
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Setup Instructions

Follow these steps to clone the repository and run the Docker stack:

1. **Clone the Repository**  
   Run the following command to clone the repository:
   ```bash
   git clone https://github.com/Nikolay-Toshev/PharmaQ.git

2. **Navigate to the Project Directory**  
   Move into the project directory:
   ```bash
   cd ./PharmaQ/PharmaQ

3. **Build and Start the Docker Containers**  
   Build and run the application with Docker Compose:
   ```bash
   docker-compose up --build

3. **Restart the Docker Containers**
   After the application is up and running for the first time, you must restart the containers to apply the necessary database migrations: 
   Press Ctrl+C to stop the application.
   Run the following command to restart it:
   ```bash
   docker-compose up --build
