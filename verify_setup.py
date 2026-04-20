import sys, subprocess, os, shutil
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

checks = {
    'Python 3.11'  : sys.version.startswith('3.11'),
    'py-solc-x'    : len(__import__('solcx').get_installed_solc_versions()) > 0,
    'API Key'      : bool(os.getenv('ETHERSCAN_API_KEY')),
}

node = subprocess.run(['node', '--version'], capture_output=True, text=True)
npx_path = shutil.which('npx')
hh = subprocess.run(
    [npx_path, 'hardhat', '--version'],
    capture_output=True, text=True,
    cwd=os.path.join(os.path.dirname(__file__), 'hardhat_project')
)

checks['Node.js v24'] = node.returncode == 0
checks['Hardhat']     = hh.returncode == 0

print('=== VERIFIKASI SETUP ===')
for label, ok in checks.items():
    icon = 'OK' if ok else 'FAIL'
    print(f'  [{icon}] {label}')

print()
all_ok = all(checks.values())
print('Siap lanjut ke notebook!' if all_ok else 'Ada yang belum siap - cek tanda FAIL')
print()
print(f'  Node   : {node.stdout.strip()}')
print(f'  Hardhat: {hh.stdout.strip()}')
print(f'  solc   : {__import__("solcx").get_installed_solc_versions()}')
