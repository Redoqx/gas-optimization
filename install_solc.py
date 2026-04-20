import solcx
print('Installing solc 0.8.20...')
solcx.install_solc('0.8.20')
solcx.set_solc_version('0.8.20')
print('Done:', solcx.get_solc_version())
