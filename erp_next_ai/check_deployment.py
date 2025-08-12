#!/usr/bin/env python3
"""
배포 준비 상태 확인 스크립트
ERPNext AI System의 배포 준비 상태를 확인합니다.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# 색상 출력을 위한 ANSI 코드
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """헤더 출력"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_check(description: str, status: bool, details: str = ""):
    """체크 결과 출력"""
    icon = f"{Colors.GREEN}✅" if status else f"{Colors.RED}❌"
    print(f"{icon} {description}{Colors.END}")
    if details:
        print(f"   {Colors.CYAN}📝 {details}{Colors.END}")

def check_file_exists(file_path: str, description: str) -> bool:
    """파일 존재 확인"""
    exists = Path(file_path).exists()
    print_check(description, exists, f"경로: {file_path}")
    return exists

def check_git_status() -> Dict[str, bool]:
    """Git 상태 확인"""
    print_header("🔍 Git 상태 확인")
    
    results = {}
    
    try:
        # Git 저장소 확인
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True, cwd='.')
        is_git_repo = result.returncode == 0
        print_check("Git 저장소 초기화", is_git_repo)
        results['git_repo'] = is_git_repo
        
        if is_git_repo:
            # 원격 저장소 확인
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, cwd='.')
            has_origin = result.returncode == 0
            print_check("GitHub 원격 저장소 연결", has_origin, 
                       f"URL: {result.stdout.strip()}" if has_origin else "")
            results['git_origin'] = has_origin
            
            # 커밋 상태 확인
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd='.')
            is_clean = len(result.stdout.strip()) == 0
            print_check("작업 디렉토리 정리 상태", is_clean)
            results['git_clean'] = is_clean
            
    except Exception as e:
        print_check("Git 명령어 실행", False, f"오류: {e}")
        results.update({'git_repo': False, 'git_origin': False, 'git_clean': False})
    
    return results

def check_backend_files() -> Dict[str, bool]:
    """백엔드 파일 구조 확인"""
    print_header("🔧 백엔드 파일 구조 확인")
    
    backend_files = {
        'main.py': 'backend/main.py',
        'requirements.txt': 'backend/requirements.txt',
        'Dockerfile': 'backend/Dockerfile',
        'railway.toml': 'backend/railway.toml',
        '.env.example': 'backend/.env.example',
        'alembic.ini': 'backend/alembic.ini',
        'migrations/env.py': 'backend/migrations/env.py',
    }
    
    results = {}
    for name, path in backend_files.items():
        results[f'backend_{name}'] = check_file_exists(path, f"백엔드 {name}")
    
    return results

def check_frontend_files() -> Dict[str, bool]:
    """프론트엔드 파일 구조 확인"""
    print_header("🌐 프론트엔드 파일 구조 확인")
    
    frontend_files = {
        'package.json': 'frontend/package.json',
        'vite.config.js': 'frontend/vite.config.js',
        'vercel.json': 'frontend/vercel.json',
        '.env.example': 'frontend/.env.example',
        'index.html': 'frontend/index.html',
        'src/main.js': 'frontend/src/main.js',
        'src/App.vue': 'frontend/src/App.vue',
    }
    
    results = {}
    for name, path in frontend_files.items():
        results[f'frontend_{name}'] = check_file_exists(path, f"프론트엔드 {name}")
    
    return results

def check_documentation() -> Dict[str, bool]:
    """문서 파일 확인"""
    print_header("📚 문서 파일 확인")
    
    docs = {
        'README.md': 'README.md',
        'DEPLOYMENT_GUIDE.md': 'DEPLOYMENT_GUIDE.md',
        'AI_API_SETUP.md': 'AI_API_SETUP.md',
        'DATABASE_SETUP.md': 'DATABASE_SETUP.md',
        'QUICKSTART.md': 'QUICKSTART.md',
    }
    
    results = {}
    for name, path in docs.items():
        results[f'docs_{name}'] = check_file_exists(path, f"문서 {name}")
    
    return results

def check_package_json() -> Dict[str, bool]:
    """package.json 설정 확인"""
    print_header("📦 Frontend package.json 확인")
    
    package_path = Path('frontend/package.json')
    results = {'package_json_exists': False, 'package_json_valid': False}
    
    if not package_path.exists():
        print_check("package.json 존재", False)
        return results
    
    results['package_json_exists'] = True
    
    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # 필수 스크립트 확인
        required_scripts = ['dev', 'build', 'preview']
        has_scripts = all(script in package_data.get('scripts', {}) 
                         for script in required_scripts)
        print_check("빌드 스크립트 설정", has_scripts, 
                   f"스크립트: {list(package_data.get('scripts', {}).keys())}")
        
        # 필수 의존성 확인
        required_deps = ['vue', '@vitejs/plugin-vue', 'vite']
        has_deps = all(dep in package_data.get('dependencies', {}) or 
                      dep in package_data.get('devDependencies', {})
                      for dep in required_deps)
        print_check("필수 의존성 설정", has_deps)
        
        results['package_json_valid'] = has_scripts and has_deps
        
    except Exception as e:
        print_check("package.json 파싱", False, f"오류: {e}")
        results['package_json_valid'] = False
    
    return results

def check_environment_examples() -> Dict[str, bool]:
    """환경변수 예제 파일 확인"""
    print_header("🔧 환경변수 설정 확인")
    
    results = {}
    
    # 백엔드 .env.example 확인
    backend_env = Path('backend/.env.example')
    if backend_env.exists():
        with open(backend_env, 'r', encoding='utf-8') as f:
            content = f.read()
            has_db_url = 'DATABASE_URL' in content
            has_openai = 'OPENAI_API_KEY' in content
            has_anthropic = 'ANTHROPIC_API_KEY' in content
            
            print_check("백엔드 환경변수 예제", True)
            print_check("  - 데이터베이스 URL", has_db_url)
            print_check("  - OpenAI API 키", has_openai)
            print_check("  - Anthropic API 키", has_anthropic)
            
            results['backend_env'] = has_db_url and has_openai and has_anthropic
    else:
        print_check("백엔드 환경변수 예제", False)
        results['backend_env'] = False
    
    # 프론트엔드 .env.example 확인
    frontend_env = Path('frontend/.env.example')
    if frontend_env.exists():
        with open(frontend_env, 'r', encoding='utf-8') as f:
            content = f.read()
            has_api_url = 'VITE_API_URL' in content
            has_ai_copilot = 'VITE_ENABLE_AI_COPILOT' in content
            
            print_check("프론트엔드 환경변수 예제", True)
            print_check("  - API URL", has_api_url)
            print_check("  - AI 코파일럿 설정", has_ai_copilot)
            
            results['frontend_env'] = has_api_url and has_ai_copilot
    else:
        print_check("프론트엔드 환경변수 예제", False)
        results['frontend_env'] = False
    
    return results

def generate_deployment_summary(all_results: Dict[str, Dict[str, bool]]):
    """배포 준비 상태 요약"""
    print_header("📊 배포 준비 상태 요약")
    
    # 전체 결과 집계
    total_checks = 0
    passed_checks = 0
    
    for category, results in all_results.items():
        for check, status in results.items():
            total_checks += 1
            if status:
                passed_checks += 1
    
    success_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"📈 전체 성공률: {Colors.BOLD}{success_rate:.1f}%{Colors.END} ({passed_checks}/{total_checks})")
    
    if success_rate >= 90:
        status_color = Colors.GREEN
        status_text = "🚀 배포 준비 완료!"
        recommendation = "모든 준비가 완료되었습니다. 배포를 진행하세요."
    elif success_rate >= 70:
        status_color = Colors.YELLOW
        status_text = "⚠️ 일부 수정 필요"
        recommendation = "몇 가지 항목을 수정한 후 배포하세요."
    else:
        status_color = Colors.RED
        status_text = "❌ 추가 작업 필요"
        recommendation = "배포 전에 더 많은 준비 작업이 필요합니다."
    
    print(f"\n{status_color}{Colors.BOLD}{status_text}{Colors.END}")
    print(f"{Colors.CYAN}💡 권장사항: {recommendation}{Colors.END}")
    
    # 실패한 항목들 나열
    failed_items = []
    for category, results in all_results.items():
        for check, status in results.items():
            if not status:
                failed_items.append(f"{category}.{check}")
    
    if failed_items:
        print(f"\n{Colors.RED}🔧 수정 필요 항목:{Colors.END}")
        for item in failed_items[:10]:  # 최대 10개만 표시
            print(f"   - {item}")
        if len(failed_items) > 10:
            print(f"   ... 및 {len(failed_items) - 10}개 추가")

def main():
    """메인 함수"""
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("🤖 ERPNext AI System - 배포 준비 상태 확인")
    print(f"{'='*60}{Colors.END}")
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    print(f"{Colors.CYAN}📁 현재 디렉토리: {current_dir}{Colors.END}")
    
    # 각 항목 확인
    all_results = {}
    all_results['git'] = check_git_status()
    all_results['backend'] = check_backend_files()
    all_results['frontend'] = check_frontend_files()
    all_results['package'] = check_package_json()
    all_results['environment'] = check_environment_examples()
    all_results['documentation'] = check_documentation()
    
    # 최종 요약
    generate_deployment_summary(all_results)
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}🔗 다음 단계:{Colors.END}")
    print("1. Railway (https://railway.app)에서 GitHub 저장소 연결")
    print("2. Vercel (https://vercel.com)에서 GitHub 저장소 연결")
    print("3. 환경변수 설정")
    print("4. 배포 실행")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 준비 완료 후 deploy.bat 실행하여 배포를 시작하세요!{Colors.END}")

if __name__ == "__main__":
    main()