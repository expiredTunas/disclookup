# Imports
from argparse import ArgumentParser, RawDescriptionHelpFormatter, ArgumentTypeError
from colorama import Fore, Back, Style
import httpx
import json

# Basic information that appears when you add -h
__version__ = "0.0.1"
module_name = "Discord ID lookup for CLI."

# Getting bot token from token.txt
token: str
with open('token.txt', 'r') as f:
	contents = f.read()
	token = contents.strip() #removes newlines


# Header for authorization. The bot token provided in the .txt file will be used here.
header = {'Content-Type': 'application/json',
			'Authorization': f'Bot {token}'}

# Defining ID lookup function.
def idlookup(id):
	try:
		raw = httpx.get(f'https://discord.com/api/users/{id}', headers=header)
		raw.raise_for_status()
	except httpx.HTTPStatusError as exc:
		print(f"{Fore.RED}Error response:{Fore.RESET} {exc.response.status_code}")
		exit()

	json = raw.json()
	return json

# Converts flag (as an integer) value to a list
def flagconvert(flag):
	flaglist = {'Active_Developer': 4194304,
	'Bot_HTTP_Interactions': 524288,
	'Certified_Moderator': 262144,
	'Verified_Developer': 131072,
	'Verified_Bot': 65536,
	'Bug_Hunter_Level_2' : 16384,
	'Team_User' : 1024,
	'Early_Supporter' : 512,
	'House_Balance' : 256,
	'House_Brilliance' : 128,
	'House_Bravery' : 64,
	'Bug_Hunter_Level_1' : 8,
	'HypeSquad' : 4,
	'Partnered_Server_Owner' : 2,
	'Discord_Employee' : 1}

	flist = []
	fcalc = 0
	for i in flaglist:
		if (flaglist[i] + fcalc) <= flag:
			fcalc = fcalc + flaglist[i]
			flist.append(i)
	
	return flist

# Processing the json for a nicer output.
def json_process(json, id):
	for i in list(json):
		if 'flags' in i:
			if json[i] <= 0:
				json[i] = 'None'
			else:
				json[i] = flagconvert(json[i])
				for ind, ite in enumerate(json[i]):
					json[i][ind] = ite.replace('_', ' ').capitalize()

		if i in ('avatar') and not None:
			json[i] = f'https://cdn.discordapp.com/avatars/{id}/{json[i]}'
		elif i in ('banner') and not None:
			json[i] = f'https://cdn.discordapp.com/avatars/{id}/{json[i]}'
		
		json[i.capitalize()] = json.pop(i)
		
		if '_' in i:
			json[i.replace('_', ' ').capitalize()] = json.pop(i.capitalize())
	
	return json

# The main code
def main():
	parser = ArgumentParser(
		formatter_class=RawDescriptionHelpFormatter,
		description=f"{module_name} Version: {__version__}"
	)

	parser.add_argument('userid', help='The ID of the user you are looking up information on.', type=int)
	parser.add_argument('--raw', '-r', help='Outputs raw json instead of something more readable.', action='store_true', dest='raw')
    
	args = parser.parse_args()
      
	print(f'{Fore.BLUE} Looking up the ID:{Fore.RESET} {args.userid}')
	json = idlookup(args.userid)

	if args.raw:
		if json:
			print(f'{Fore.CYAN}{json}{Fore.RESET}')
			exit()

	if json:
		processed = json_process(json, args.userid)
		for i in processed:
			print(f'{Fore.BLUE}{i} :{Fore.RESET} {processed[i]}')
		


if __name__ == "__main__":
	main()