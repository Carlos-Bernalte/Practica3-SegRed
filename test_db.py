import requests
import json
import urllib3
import uuid
# urllib3.disable_warnings()

uri = 'https://myserver.local:5000'

headersList = {
 "Content-Type": "application/json" 
}


def signup_user(username, password):
    # Test signup
    payload = json.dumps({
      "username":username,
      "password":password
    })
    response = requests.request("POST", uri+'/signup', data=payload,  headers=headersList, verify='cert/cert.pem')
    
    if response.status_code == 201:
        print('Signup for user',username,'OK')
        print('Token:',response.text)
        return response.json()['access_token']
    else:
        print('Signup Error')
        print(response.text)
        return None

def login_user(username, password):
    # Test login
    payload = json.dumps({
      "username":username,
      "password":password
    })
    response = requests.request("POST", uri+'/login', data=payload,  headers=headersList, verify='cert/cert.pem')
    
    if response.status_code == 200:
        print('Login for user',username,'OK')
        print('Token:',response.text)
        return response.json()['access_token']
    else:
        print('Login Error')
        print(response.text)
        return None

def post_random_doc(username, token):
    # Test post doc

    payload = json.dumps({
      "doc_content":"This is a random doc"
    })
    headersList['Authorization'] = 'token '+token
    doc_id = str(uuid.uuid4())[:5]

    response = requests.request("POST", uri+'/'+username+'/'+doc_id, data=payload,  headers=headersList, verify='cert/cert.pem')
    if response.status_code == 201:
        print('Post doc for user',username,'OK')
        print(response.text)
        return doc_id
    else:
        print('Post doc Error')
        print(response.text)
        return None

def get_doc(username, token, doc_id):
    if doc_id is None:
        return
    # Test get doc
    headersList['Authorization'] = 'token '+token
    
    response = requests.request("GET", uri+'/'+username+'/'+doc_id,  headers=headersList, verify='cert/cert.pem')
    if response.status_code == 200:
        print('Get doc for user',username,'OK')
        print(response.text)
    else:
        print('Get doc Error')
        print(response.text)

def update_doc(username, token, doc_id):
    if doc_id is None:
        return
    # Test update doc
    payload = json.dumps({
      "doc_content":"This is a random doc updated"
    })
    headersList['Authorization'] = 'token '+token
    
    response = requests.request("PUT", uri+'/'+username+'/'+doc_id, data=payload,  headers=headersList, verify='cert/cert.pem')
    if response.status_code == 200:
        print('Update doc',doc_id,'for user',username,'OK')
        print(response.text)
    else:
        print('Update doc Error')
        print(response.text)

def delete_doc(username, token, doc_id):
    if doc_id is None:
        return
    # Test delete doc
    headersList['Authorization'] = 'token '+token
    
    response = requests.request("DELETE", uri+'/'+username+'/'+doc_id,  headers=headersList, verify='cert/cert.pem')
    if response.status_code == 200:
        print('Delete doc',doc_id,'for user',username,'OK')
        print(response.text)
    else:
        print('Delete doc Error')
        print(response.text)

def get_all_docs(username, token):
    # Test get all docs
    headersList['Authorization'] = 'token '+token
    
    response = requests.request("GET", uri+'/'+username,  headers=headersList, verify='cert/cert.pem')
    if response.status_code == 200:
        print('Get all docs for user',username,'OK')
        print(response.text)
    else:
        print('Get all docs Error')
        print(response.text)


if __name__ == '__main__':
  # Test signup
  print('---------------Test signup---------------')
  signup_user('test1', 'test')
  signup_user('test2', 'test')
  signup_user('test3', 'test3')

  # Test login
  print('---------------Test login---------------')
  token1=login_user('test1', 'test')
  token2=login_user('test2', 'test')
  token3=login_user('test3', 'test3')

  # Test post doc
  print('---------------Test post doc---------------')
  for i in range(0, 10):
      doc1=post_random_doc('test1', token1)
      doc2=post_random_doc('test2', token2)
      doc3=post_random_doc('test3', token3)

  # Test get doc
  print('---------------Test get doc---------------')
  get_doc('test1', token1, doc1)
  get_doc('test2', token2, doc2)
  get_doc('test3', token3, doc3)

  # Test update doc
  print('---------------Test update doc---------------')
  update_doc('test1', token1, doc1)
  update_doc('test2', token2, doc2)
  update_doc('test3', token3, doc3)

  # Test get all docs after update
  print('---------------Test get all docs after update---------------')
  get_all_docs('test1', token1)
  get_all_docs('test2', token2)
  get_all_docs('test3', token3)

  # Test delete doc
  print('---------------Test delete doc---------------')
  delete_doc('test1', token1, doc1)
  delete_doc('test2', token2, doc2)
  delete_doc('test3', token3, doc3)

  # Test get all docs after delete
  print('---------------Test get all docs after delete---------------')
  get_all_docs('test1', token1)
  get_all_docs('test2', token2)
  get_all_docs('test3', token3)


