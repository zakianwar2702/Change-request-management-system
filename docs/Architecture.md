# System Architecture

## Overview

The Change Management System follows a three-tier architecture consisting of the Presentation Layer, Application Layer, and Database Layer.

## Architecture Components

### Presentation Layer
- React.js
- HTML
- CSS
- JavaScript

This layer provides the user interface for interacting with the system.

### Application Layer
- Django
- REST API

This layer processes user requests, implements business logic, and communicates with the database.

### Database Layer
- SQLite

This layer stores user information, change requests, ticket details, and approval records.

## Workflow

User → React Frontend → Django Backend → SQLite Database → Response to User