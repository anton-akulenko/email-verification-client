"""This module contains functions for email and domain verification."""
from typing import Dict, Any

import requests
import json

API_KEY: str = '93072a33112358841b7225e00dd324382226106b'

class HunterClient:
    def __init__(self, api_key: str = API_KEY, base_url: str = 'https://api.hunter.io/v2/'):
        self.api_key = api_key
        self.base_url = base_url
        self.email_results: Dict[str, Dict[str, Any]] = {}
        self.domain_results: Dict[str, Dict[str, Any]] = {}

    def _make_request(self, url, payload):
        r = requests.get(url, params=payload)
        data = r.json()
        # Raise error if not 200 OK
        r.raise_for_status()

        return data

    def verify_email(self, email: str) -> Dict[str, Any]:
        """Verify the provided email address."""
        url = f'{self.base_url}email-verifier'
        payload = {'api_key': self.api_key, 'email': email}
        try:
            data = self._make_request(url, payload)
            return data['data']['status'], data['meta']
        except data.RequestException as error_msg:
            return {'error': f'Request failed: {str(error_msg)}'}

    def save_email_result(self, email: str) -> str:
        try:
            self.email_results[email] = self.verify_email(email)
        except Exception as e:
            print('Error during exist request: {}'.format(e))
        return print(email, json.dumps(self.email_results[email], indent=2))

    def get_email_results(self) -> Dict[str, Dict[str, Any]]:
        return print(json.dumps(self.email_results, indent=2))
    
    def get_one(self, email: str) -> str:
        """Get one Email results."""
        if email in self.email_results:
            return print(email, json.dumps(self.email_results[email], indent=2))
        return print({'error': 'Email not found'})

    def update_email_result(self, email: str, upd: Dict[str, Any]) -> str:
        """Update one Email results."""
        if email in self.email_results:
            self.email_results[email] = upd
            print(f'Email: {email}  successfully updated!')
            return print(json.dumps(self.email_results[email], indent=2))

        return print({'error': 'Email not found'})

    def create_email_result(self, email: str, upd: Dict[str, Any]) -> str:
        """Update one Email results."""
        if email not in self.email_results:
            self.email_results[email] = upd
            print(f'Email: {email}  successfully created!')
            return print(json.dumps(self.email_results[email], indent=2))

        return print(f'Email: {email} already exist')

    def delete_email_result(self, email: str) -> str:
        """Remove  Email results."""
        if email in self.email_results:
            removed_data = self.email_results.pop(email)
            print(f'Email: {email} successfully deleted!')
            return  print("Removed data: ", json.dumps(removed_data, indent=2))
        return print('Email not found', email)

def main():
    client = HunterClient()
    print("Available commands (verify, create, show_all, show_one, update, delete):")
    while True:
        command = input("Enter the number of the command: ")
        if command == 'verify':
            email = input("Enter email: ")
            if email:
                print('Checking if {} exists'.format(email))
                client.save_email_result(email)
            else:
                print('email is required when using the verify command')

        elif command == 'create':
            email = input("Enter email: ")
            data = input("Enter data in format {'status': 'verified', 'some_data': 'some_data'...}: ")
            if email:
                client.create_email_result(email, data)
            else:
                print('email is required when using the create command')

        elif command == 'show_all':
            client.get_email_results()

        elif command == 'show_one':
            email = input("Enter email: ")
            if email:
                client.get_one(email)
            else:
                print('email is required when using the show_one command')

        elif command == 'update':
            email = input("Enter email: ")
            data = input("Enter data {'status': 'verified'}: ")
            if email:
                client.update_email_result(email, data)
            else:
                print('email is required when using the update command')

        elif command == 'delete':
            email = input("Enter email: ")
            if email:
                client.delete_email_result(email)
            else:
                print('email is required when using the delete command')
            
        elif command == 'exit':
            print("Bye!") 
            break 
        else:
            print('Invalid command {}'.format(command))



if __name__ == '__main__':
    main()

