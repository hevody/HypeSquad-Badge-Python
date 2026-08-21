import requests
import json
import os

### reading configs ###
with open('config.json') as f:
  config = json.load(fp=f)

if os.name == 'nt': 
  clear = config["clear_windows"]

if os.name == 'posix':
  clear = config["clear_posix"]

url = config["API_URL"]
headers = config["HEADERS"]
payload = config["PAYLOAD"]

### validation ###
def provide_discord_token() -> str:
  os.system(clear)
  print(config["discord_token_instruction"])
  user_discord_token = input("\nDISCORD_TOKEN: ")
  return user_discord_token

def determine_the_house() -> int:
  hypesquad_house = {"1": "HypeSquad Bravery",
                   "2": "HypeSquad Brilliance",
                   "3": "HypeSquad Balance"}

  house_chosen = False
  input_validation_helper = ''

  while not house_chosen:
    os.system(clear)
    print(f'''
    Which HypeSquad House you want to be a part of?
    ''')

    for choice in hypesquad_house.keys():
      print(f'    [{choice}] {hypesquad_house[choice]}')
    print(input_validation_helper)

    try:
      desired_hypesquad = input('\n> ')
    except KeyboardInterrupt: 
      exit()

    try:
      desired_hypesquad = int(desired_hypesquad)
      if desired_hypesquad > 3 or desired_hypesquad < 1:
        input_validation_helper = config["hype_squad_validator"]
      else:
        desired_hypesquad_pass = desired_hypesquad
        house_chosen = True
    except ValueError:
        checkIfHypeSquadStringExist = [k for k, v in hypesquad_house.items() if v.lower() == desired_hypesquad.lower()]
        if not checkIfHypeSquadStringExist:
          input_validation_helper = config["hype_squad_validator"]
        else:
          desired_hypesquad_pass = int(checkIfHypeSquadStringExist[0])
          house_chosen = True

  return desired_hypesquad_pass

def perform_a_post_request() -> bool:
  print('\n[*] Performing a POST request to Discord.com')
  response = requests.post( url=url, 
                            json=payload,
                            headers=headers)

  if str(response) == '<Response [401]>':
    return False
  if str(response) == '<Response [204]>':
    return True
    

  return str(response)

if __name__ == '__main__':
  headers["Authorization"] = provide_discord_token()
  config["PAYLOAD"]["house_id"] = determine_the_house()
  success = perform_a_post_request()

  if success:
    print('Success! You can now view the badge in your profile')
  if not success:
    print('Check if you pasted your Discord token right...')