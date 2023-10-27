# imports:
import requests
import json
from concurrent.futures import ThreadPoolExecutor



"""
@ABOUT:  This file simulate a plugin for the: dummyapi.io REST API service.
@AUTHOR: Itamar Kuznitsov.
@SINCE:  Oct 2023.

"""


# represent the dummyapi plugin
class DUMMYAPI_PLUGIN:  
    # plugin constructor 
    def __init__(self, api_key) -> None:
        self.base_url = "https://dummyapi.io/data/v1/"
        self.headers = {'app-id': api_key}

    
    # try to connect to the dummyapi api   
    def test_connection(self) -> str:
        try:
            response = requests.get(self.base_url + 'user', headers= self.headers)
            # check status
            response.raise_for_status()
            # save response data in json file for testing purposes 
            self.save_to_file(response.json(), 'test_connection_response.json') 
            # return response status
            return str(response)
            
        except requests.exceptions.RequestException as err:
            print(f"Error occurred during the request: {err}")
            return str(err)


    # collect data of all the users in the system  
    def collect_all_users(self) -> int:
        all_users = []
        page = 0
        limit = 50 # the maximum amount, 20 is the default.

        # paginating mechanism - run throught all pages and collect data 
        while True:
            try:
                param = {'page': page, 'limit': limit}
                response = requests.get(self.base_url + 'user', headers= self.headers, params= param)
                # check status, should be 200 in good case
                response.raise_for_status()  
                users = response.json().get('data', [])
                # no more users - break
                if not users:
                    break 
                # otherwise - add to the list of all users
                all_users.extend(users)
                page += 1
            
            except requests.exceptions.RequestException as err:
                print(f"An error occurred during the request: {err}")
                break 
        
        # save all users data in a new json file and return the function status
        file_status = self.save_to_file(all_users, 'users_data.json')
        return file_status



    # fetching 50 posts
    def fetch_posts(self, limit= 50) -> list:
        all_posts = []
        page = 0

        # collect "limit" amount of posts
        while len(all_posts) < limit:
            try:
                param = {'page': page, 'limit': limit}
                response = requests.get(self.base_url + 'post', headers= self.headers, params=param)
                response.raise_for_status()  
                posts = response.json().get('data', [])
                if not posts:
                    break  
            
                all_posts.extend(posts)
                page += 1

            except requests.exceptions.RequestException as err:
                print(f"An error occurred during the request: {err}")
                break 
        
        return all_posts



    # fetch the comments of given post based on its post_id
    def fetch_comments_for_post(self, post_id):
        try:
            response = requests.get(self.base_url + f'post/{post_id}/comment', headers=self.headers)
            response.raise_for_status() 
            comments = response.json().get('data', [])
            return comments
        
        except requests.exceptions.RequestException as err:
            print(f"An error occurred while fetching comments for post {post_id}: {err}")
            return []
        

    # collect 50 posts with their comments from the system  
    def collect_posts_and_comments(self) -> int:
        # fetch 50 posts data
        all_posts = self.fetch_posts()
        
        # if got posts:
        if all_posts:
            # for each post fetch the comment
            for post in all_posts:
                post_id = post['id']
                comments = self.fetch_comments_for_post(post_id)
                # add comments to the fetched post
                post['comments'] = comments
            
            # save all posts and comments data in a new json file
            file_status = self.save_to_file(all_posts, 'posts_with_comments.json')
            return file_status

        else:
            print("No posts data fetched.")
            # for error representation
            return 1


    # assistance function to write data in a new json file 
    def save_to_file(self, data, filename) -> int:
        if data:
            try:
                with open(filename, 'w') as file:
                    json.dump(data, file)
                # if success
                return 0  
            
            except Exception as err:
                print(f"Error occurred while writing to the file: {err}")
        return 1

# end of DUMMYAPI_PLUGIN class




# entrypoint to run the program 
if __name__ == "__main__":
    # the customer's access token  
    api_key = input("Enter your api key: ") 
    # build the plugin
    dummyapi_plugin = DUMMYAPI_PLUGIN(api_key)

    # another plugin with non-valid api key 
    non_valid_dummyapi_plugin = DUMMYAPI_PLUGIN(api_key+'0')

    # test the api connection - return the status
    valid_key_status = dummyapi_plugin.test_connection()
    non_valid_key_status = non_valid_dummyapi_plugin.test_connection()
    
    # return 0 for successful collection otherwise 1
    collect_users_status = dummyapi_plugin.collect_all_users()

    collect_posts_status = dummyapi_plugin.collect_posts_and_comments()

    

    # TODO(I): for programing
    print("[+] Test valid api key connection status:  " + valid_key_status)
    print("[+] Test non-valid api key connection status:  " + non_valid_key_status)
    print("[+] Users evidencne collection status:  " + str(collect_users_status))
    print("[+] Posts evidencne collection status:  " + str(collect_posts_status))


    




'''
Another version of fetching 50 posts - using threadpool.
Fuster but can cause problem (due to api's rate limit) with the api service, so I choose not using it.
'''

    # # fetching 50 posts
    # def fetch_posts(self, limit= 50) -> list:
    #     all_posts = []
    #     page = 0

    #     # collect "limit" amount of posts
    #     while len(all_posts) < limit:
    #         try:
    #             param = {'page': page, 'limit': limit}
    #             response = requests.get(self.base_url + 'post', headers= self.headers, params=param)
    #             response.raise_for_status()  
    #             posts = response.json().get('data', [])
    #             if not posts:
    #                 break  
            
    #             all_posts.extend(posts)
    #             page += 1

    #         except requests.exceptions.RequestException as err:
    #             print(f"An error occurred during the request: {err}")
    #             break 
        
    #     return all_posts



    # # fetch the comments of given post based on its post_id
    # def fetch_comments_for_post(self, post):
    #     try:
    #         post_id = post['id']
    #         response = requests.get(self.base_url + f'post/{post_id}/comment', headers=self.headers)
    #         response.raise_for_status() 
    #         comments = response.json().get('data', [])
    #         post['comments'] = comments
    #         return post
        
    #     except requests.exceptions.RequestException as err:
    #         print(f"An error occurred while fetching comments for post {post_id}: {err}")
    #         return []


    # # collect 50 posts with their comments from the system  
    # def collect_posts_and_comments(self) -> int:
    #     # fetch 50 posts data
    #     posts = self.fetch_posts()

    #     # create a ThreadPoolExecutor
    #     max_worker_threads = 10
    #     with ThreadPoolExecutor(max_workers= max_worker_threads) as executor:
    #         all_posts_with_comments = list(executor.map(self.fetch_comments_for_post, posts))

    #     # save the merged data to a json file
    #     file_status = self.save_to_file(all_posts_with_comments, 'posts_with_comments.json')
    #     return file_status


