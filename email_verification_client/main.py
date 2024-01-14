"""This module contains functions for email and domain verification."""
from typing import Dict, Any
import requests
import json
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


# API_KEY: str = '93072a33112358841b7225e00dd324382226106b'
API_KEY: str = ''
COMMANDS: list = ['verify', 'create', 'show_all', 'show_one', 'update', 'delete', 'exit']


class EmailStorage:
    def __init__(self):
      
        self.email_results: Dict[str, Dict[str, Any]] = {}

    def save_email_result(self, email: str, result: Dict[str, Any]) -> None:
        self.email_results[email] = result

    def get_email_results(self) -> Dict[str, Dict[str, Any]]:
        return self.email_results

    def get_one(self, email: str) -> Dict[str, Any]:
        return self.email_results.get(email)

    def update_email_result(self, email: str, upd: Dict[str, Any]) -> None:
        if email in self.email_results:
            self.email_results[email] = upd

    def create_email_result(self, email: str, upd: Dict[str, Any]) -> None:
        if email not in self.email_results:
            self.email_results[email] = upd

    def delete_email_result(self, email: str) -> None:
        if email in self.email_results:
            del self.email_results[email]


class HunterClient:
    def __init__(self, api_key: str = API_KEY, base_url: str = 'https://api.hunter.io/v2/'):
        self.api_key = api_key
        self.base_url = base_url
        self.storage = EmailStorage()  
    
    def _make_request(self, url, payload):
        req_data = requests.get(url, params=payload)
        data = req_data.json()
        req_data.raise_for_status()

        return data

    def is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not bool(re.match(pattern, email)):
            return print('Empty or invalid email format. Example: example@example.com')
        return True

    def verify_email(self, email: str) -> Dict[str, Any]:
        url = f'{self.base_url}email-verifier'
        payload = {'api_key': self.api_key, 'email': email}
        try:
            return self._make_request(url, payload)
        except requests.RequestException as error_msg:
            return print({'error': f'Request failed: {str(error_msg)}'})

    def save_email_result(self, email: str) -> None:
        try:
            result = self.verify_email(email)
            self.storage.save_email_result(email, result)
            print(email, json.dumps(result, indent=2))
        except Exception as err:
            print('Error, exist : {}'.format(err))

    def get_email_results(self) -> Dict[str, Dict[str, Any]]:
        return print(json.dumps(self.storage.get_email_results(), indent=2))
        
    def get_one(self, email: str) -> None:
        result = self.storage.get_one(email)
        if result:
            print(email, json.dumps(result, indent=2))
        else:
            print({'error': 'Email not found'})

    def update_email_result(self, email: str, upd: Dict[str, Any]) -> None:

        self.storage.update_email_result(email, upd)
        result = self.storage.get_one(email)
        if result:
            print('Email: {} successfully updated!'.format(email))
            print(json.dumps(result, indent=2))
        else:
            print({'error': 'Email not found'})

    def create_email_result(self, email: str, upd: Dict[str, Any]) -> None:
        self.storage.create_email_result(email, upd)
        result = self.storage.get_one(email)
        if result:
            print('Email: {} successfully created!'.format(email))
            print(json.dumps(result, indent=2))
        else:
            print('Email: {} already exists'.format(email))

    def delete_email_result(self, email: str) -> None:
        result = self.storage.get_one(email)
        if result:
            self.storage.delete_email_result(email)
            print('Email: {} successfully deleted!'.format(email))
            print('Removed data: ', json.dumps(result, indent=2))
        else:
            print('Email: {} not found'.format(email))

def main():
    API_KEY: str = prompt('Please enter your API_KEY for hunter.io to continue: ')
    client = HunterClient(API_KEY)
    command_completer = WordCompleter(COMMANDS)
    print('Available commands (verify, create, show_all, show_one, update, delete): ')
    while True:
        command = prompt('Enter the command: ', completer=command_completer)
        match command:
            case 'verify':
                email = prompt('Enter email: ')
                if client.is_valid_email(email):
                    print('Checking if {} exists'.format(email))
                    client.save_email_result(email)

            case 'create':
                email = prompt('Enter email: ')
                data = prompt("Enter data in format {'status': 'verified', 'some_data': 'some_data'...}: ")
                if client.is_valid_email(email):
                    client.create_email_result(email, data)

            case 'show_all':
                client.get_email_results()

            case 'show_one':
                email = prompt('Enter email: ')
                if email:
                    client.get_one(email)

            case 'update':
                email = prompt('Enter email: ')
                data = prompt("Enter data {'status': 'verified'}: ")
                if client.is_valid_email(email):
                    client.update_email_result(email, data)

            case 'delete':
                email = prompt('Enter email: ')
                if client.is_valid_email(email):
                    client.delete_email_result(email)

            case 'exit':
                print('Bye!') 
                break
            case _:
                print(f'Invalid command \033[1m"{command}"\033[0m\nPlease enter a valid command: {", ".join(COMMANDS)}')


if __name__ == '__main__':
    main()
