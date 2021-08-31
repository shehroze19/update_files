from jira import JIRA
import requests
import time
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

class JiraException(Exception):
    pass

class Jira(object):
    __options = {
        'server': 'https://shozi.atlassian.net/',
            'verify': True
    }
    __client = None

    def __init__(self, **kwargs):
        if len(kwargs) != 2:
            raise JiraException(
                'In order to use this class you need to specify a user and a password as keyword arguments!')
        else:
            if 'username' in kwargs.keys():
                self.__username = kwargs['username']
            else:
                raise JiraException(
                    'You need to specify a username as keyword argument!')
            if 'password' in kwargs.keys():
                self.__password = kwargs['password']
            else:
                raise JiraException(
                    'You need to specify a password as keyword argument!')

            try:
                self.__client = JIRA(self.__options, basic_auth=(
                    self.__username, self.__password))
            except:
                raise JiraException(
                    'Could not connect to the API, invalid username or password!') from None

    def __str__(self):
        return 'Jira(username = {}, password = {}, endpoint = {}'.format(self.__username, self.__password, self.__options['server'])

    def __repr__(self):
        return 'Jira(username = {}, password = {}, endpoint = {}'.format(self.__username, self.__password, self.__options['server'])

    def __format__(self, r):
        return 'Jira(username = {}, password = {}, endpoint = {}'.format(self.__username, self.__password, self.__options['server'])

    def getProjects(self, raw=False):
        Projects = []
        for project in self.__client.projects():
            if raw:
                Projects.append(project)
            else:
                Projects.append({ 'Name': project.key, 'Description': project.name })
        return Projects

    def getIssues(self, project_name, maxResults= 3, raw = False, **kwargs):
        Issues = []
        if len(kwargs) < 0:
            raise JiraException('You need to specify a search criteria!')
        else:
            searchstring = ' '.join(
                [(_ + "=" + kwargs[_]) if _ != 'condition' else kwargs[_] for _ in kwargs])


            test=self.__client.search_issues('project='+project_name,
            startAt=0, 
            maxResults=1, 
            json_result=True)
            #this is for pagination
            total=test.get('total')
            print(total)    

                    # Define parameters for writing data
            index_beg = 0
            header = True
            mode = 'w'

                    # Search issues
            block_size = 50
            block_num = 0
            jira_search = self.__client.search_issues('project='+project_name, startAt=block_num*block_size, maxResults=block_size, fields="issuetype")

                        # Iteratively read data
            while bool(jira_search):
                # Container for Jira's data
                data_jira = []

                for issue in jira_search:
                    # Get issue key
                    issue_key = issue.key

                    # Get request type
                    request_type = str(issue.fields.issuetype)

                    # Add data to data_jira
                    data_jira.append((issue_key, request_type))

            # Write data read from Jira
                index_end = index_beg + len(data_jira)
                        # Update for the next iteration
                block_num = block_num + 1
                index_beg = index_end
                header = False
                mode = 'a'

                # Print how many issues were read
                if block_num % 50 == 0:
                    print(block_num * block_size)

                # Pause before next reading – just to be sure we will not overload Jira’s server
                time.sleep(1)    
                # New issues search
                jira_search = self.__client.search_issues('project='+project_name, startAt=block_num*block_size, maxResults=block_size,fields="issuetype")
            
            
        return data_jira

    def issueCount(self,project, **kwargs):

        test=self.__client.search_issues('project='+project, 
                   startAt=0, 
                   maxResults=1, 
                   json_result=True)
#this is for pagination
        total=test.get('total')

        total_counter=total
        
        Final_dict=[]
        while(total_counter<2):

            Final_dict.append(self.getIssues(project=project,maxResults= 1,condition='&startAt='+str(total_counter)))
            total_counter=total_counter-1

        return Final_dict

if __name__ == '__main__':
    MyJira = Jira(username='shehroze19@gmail.com', password='kteXUI9EWdsIKr9d1yXT9C7B')
    print(MyJira.getProjects())

    #Enter project name here
    print(MyJira.getIssues("test"))
