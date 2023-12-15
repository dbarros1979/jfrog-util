import requests
import csv


def get_users_in_group(api_key, base_url, group_name):
    headers = {
        'X-JFrog-Art-Api': api_key,
        'Content-Type': 'application/json'
    }

    # Get users in the specified group
    url = f'{base_url}/api/security/groups/{group_name}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    group_info = response.json()
    if 'users' in group_info:
        return group_info['users']
    else:
        return []


def export_to_csv(users, csv_filename):
    fieldnames = ['username', 'email', 'groups']  # Add more fields as needed

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow({'username': user['name'], 'email': user['email'], 'groups': ','.join(user['groups'])})


if __name__ == '__main__':
    # Set your JFrog Artifactory details
    api_key = 'YOUR_JFROG_API_KEY'
    base_url = 'https://your-artifactory-instance/artifactory'
    group_name = 'your-group-name'
    csv_filename = 'users_in_group.csv'

    users = get_users_in_group(api_key, base_url, group_name)

    if users:
        export_to_csv(users, csv_filename)
        print(f'User information exported to {csv_filename}')
    else:
        print(f'No users found in the group: {group_name}')
