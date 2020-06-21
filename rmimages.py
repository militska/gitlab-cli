import sys, requests, json, configparser, os

def main(argv):
    if len(sys.argv) > 2:
         delete_repository_by_name(name=sys.argv[1], project_id=sys.argv[2])
    else:
        print("Not all parameters are passed. The correct call format: rm_images.py private-token name_image project_id")


def delete_repository_by_name(name, project_id):
    config_gitLab = get_conf_params()['Gitlab']

    repositories = requests.get(
        "{0}/api/v4/projects/{1}/registry/repositories".format(config_gitLab['gitlab_url'], project_id),
        headers={'PRIVATE-TOKEN': config_gitLab['token']}
    ).json()

    if 'message' in repositories and repositories['message'] == '404 Project Not Found':
       print("Check the access rights of the token owner. Add ci user to members current project")
       exit()

    need_repositories = list(filter(lambda x: x["name"] == name, repositories))

    if need_repositories == []:
        print('Repository not exists, or already removed')
        exit()

    repository_id = need_repositories[0]['id']

    delete_response = requests.delete(
        "{0}/api/v4/projects/{1}/registry/repositories/{2}".format(config_gitLab['gitlab_url'], project_id, str(repository_id)),
        headers={'PRIVATE-TOKEN': config_gitLab['token']}).json()

    if delete_response == 202:
        print('Success. Repository removed')
    else:
        print('Errors: ' + json.dumps(delete_response))



def get_conf_params():
        try:
            f = open('.env')
            f.close()
        except FileNotFoundError:
            print('File .env does not exist.')

        config = configparser.ConfigParser()
        config.read(".env")

        return config


if __name__ == "__main__":
    main(sys.argv)