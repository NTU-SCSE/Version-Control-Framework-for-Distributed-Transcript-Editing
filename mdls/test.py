import os

commands = '''mkdir /Users/Nathaniel/Documents/GitHub/VCF4DTE-virtualenv/VCF4DTE/workspace
cd /Users/Nathaniel/Documents/GitHub/VCF4DTE-virtualenv/VCF4DTE/workspace
git clone git@gitlab.bretty.io:nathaniel/nathaniel.git
'''

result = os.system(commands)

print(result)
