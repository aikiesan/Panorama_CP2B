"""
Database Integration Package

A modular, SOLID-principle-based package for integrating validated biogas data
into the PanoramaCP2B database.

Modules:
    data_loaders: Load CSV/Excel files from validation notebooks
    data_validators: Validate data quality and integrity
    data_transformers: Transform data to database schema
    database_inserters: Insert data into SQLite with transactions
    integration_runner: Orchestrate the integration pipeline
"""

__version__ = "1.0.0"
__author__ = "CP2B Team - UNICAMP"
