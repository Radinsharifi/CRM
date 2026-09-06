# CRM

Customer Relationship Management system built with Django.

## Overview

This project is a modular CRM application designed to manage customer data, marketing activities, and related business processes. The system is structured with separate apps for users, marketing, and core functionality.

The project is currently under active development and serves as a foundation for a more complete enterprise CRM solution.


## Screen Shots

### Dashboard
<img width="1920" height="894" alt="Dashboard" src="https://github.com/user-attachments/assets/25a0cac5-f980-4703-923b-2abc30ee3086" />

### Customer_List
<img width="1920" height="887" alt="Customer_list" src="https://github.com/user-attachments/assets/fe423ca1-630f-49c7-84ed-f59f4ebf6cac" />

### Customer_From
<img width="1920" height="890" alt="Customer_form" src="https://github.com/user-attachments/assets/e3d25206-d74d-4eb1-a1ac-9b6c01626b7f" />

### Customer_Detail
<img width="1920" height="884" alt="Customer_detail" src="https://github.com/user-attachments/assets/45d57031-8142-4a5e-b3c2-d0fb70457115" />


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
