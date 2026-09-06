# CRM

Customer Relationship Management system built with Django.

## Overview

This project is a modular CRM application designed to manage customer data, marketing activities, and related business processes. The system is structured with separate apps for users, marketing, and core functionality.

The project is currently under active development and serves as a foundation for a more complete enterprise CRM solution.


## Screen Shots

### Dashboard
![Dashboard](https://github.com/Radinsharifi/CRM/tree/main/screenshots/dashboard.PNG)

### Customer_List
![Customer_List](https://github.com/Radinsharifi/CRM/tree/main/screenshots/Customer_list.PNG)

### Customer_From
![Customer_Form](https://github.com/Radinsharifi/CRM/tree/main/screenshots/Customer_form.PNG)

### Customer_Detail
![Customer_Detail](https://github.com/Radinsharifi/CRM/tree/main/screenshots/Customer_detail.PNG)


## Key Features

- Custom user management
- Marketing module for campaign and lead-related functionality
- Modular app structure for scalability
- Clean separation between core configuration and business logic
- Environment-based settings using python-decouple
- Standard Django admin integration

## Technical Highlights

- Multi-app architecture (`users`, `marketing`, `core`)
- Custom user model support
- Production-oriented configuration structure
- Clean URL routing and modular design
- Designed for future expansion (contacts, deals, pipelines, etc.)

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (configurable)
- **Other:** python-decouple

## Project Structure


CRM/
├── users/          # User management
├── marketing/      # Marketing and related features
├── core/           # Shared functionality
├── crm/            # Project settings and configuration
└── manage.py


## Purpose

This project demonstrates the ability to design a modular Django application with a clear structure suitable for business systems. Even in its current state, it reflects good architectural practices and a focus on maintainability.
