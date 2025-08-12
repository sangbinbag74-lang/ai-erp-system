#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple deployment readiness checker
"""

import os
from pathlib import Path

def check_file(filepath, description):
    """Check if file exists"""
    exists = Path(filepath).exists()
    status = "[OK]" if exists else "[MISSING]"
    print(f"{status} {description}: {filepath}")
    return exists

def main():
    print("="*60)
    print("ERPNext AI System - Deployment Readiness Check")
    print("="*60)
    
    # Backend files
    print("\n[BACKEND FILES]")
    backend_files = [
        ("backend/main.py", "Main application file"),
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/Dockerfile", "Docker configuration"),
        ("backend/railway.toml", "Railway deployment config"),
        ("backend/.env.example", "Environment variables example"),
        ("backend/alembic.ini", "Database migration config")
    ]
    
    backend_ok = 0
    for filepath, desc in backend_files:
        if check_file(filepath, desc):
            backend_ok += 1
    
    # Frontend files  
    print("\n[FRONTEND FILES]")
    frontend_files = [
        ("frontend/package.json", "Node.js dependencies"),
        ("frontend/vite.config.js", "Vite build configuration"),
        ("frontend/vercel.json", "Vercel deployment config"),
        ("frontend/.env.example", "Environment variables example"),
        ("frontend/src/main.js", "Main Vue.js application")
    ]
    
    frontend_ok = 0
    for filepath, desc in frontend_files:
        if check_file(filepath, desc):
            frontend_ok += 1
    
    # Documentation
    print("\n[DOCUMENTATION]")
    doc_files = [
        ("README.md", "Main project documentation"),
        ("DEPLOYMENT_GUIDE.md", "Deployment instructions"),
        ("AI_API_SETUP.md", "AI API configuration guide"),
        ("QUICKSTART.md", "Quick start guide")
    ]
    
    docs_ok = 0
    for filepath, desc in doc_files:
        if check_file(filepath, desc):
            docs_ok += 1
    
    # Summary
    total_files = len(backend_files) + len(frontend_files) + len(doc_files)
    total_ok = backend_ok + frontend_ok + docs_ok
    success_rate = (total_ok / total_files) * 100
    
    print("\n" + "="*60)
    print(f"SUMMARY: {total_ok}/{total_files} files ready ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("STATUS: Ready for deployment!")
        print("\nNext steps:")
        print("1. Run deploy.bat to open deployment dashboards")
        print("2. Connect GitHub repository to Railway")
        print("3. Connect GitHub repository to Vercel")
        print("4. Configure environment variables")
    else:
        print("STATUS: Some files are missing")
        print("Please check the missing files above")
    
    print("="*60)

if __name__ == "__main__":
    main()