import json
import requests
import urllib3
from Tests.custom_methods.CommonMethods import CommonMethods as CM

class APIMethods:

    @staticmethod
    def add_header(dict_header, header_name, header_value):
        if dict_header == "" or dict_header == None:
            dict_header = dict()
        if dict_header != {} and dict_header != None:
            dict_header[header_name] = header_value
        else:
            dict_header = { header_name: header_value}
        return dict_header

    @staticmethod
    def string_to_dict(string_value):
        if string_value != '' and string_value != None:
            dict_value = json.loads(string_value)
        else:
            dict_value = dict()
        return dict_value
    
    @staticmethod
    def api_request(method, url, params, body, headers, cookies, files, auth, timeout, allow_redirects, proxies, verify, stream, cert):
        #Scriptless to python
        url = url.replace("default:", "")
        if type(params) == str:
            params = APIMethods.string_to_dict(params)
        url = APIMethods.add_params_to_url(url, params)
        headers_for_log = headers
        if auth != None or auth != "":
            headers = APIMethods.add_header(headers, "Authorization", auth)
            auth_for_log = True
        else:
            auth_for_log = False
        ###JUST FOR VM EXECUTION
        proxies = {
        }
        if body != None and body != "" and type(body) is not dict:
            body = APIMethods.string_to_dict(body)
        environment = CM.get_value_in_temp_variable("Environment")
        verify = False
        if environment == "uat3-univ-mx":
            verify = False
        env_variables = CM.get_app_env_variable(environment)
        urllib3.disable_warnings()
        if method == 'GET':
            response = requests.get(url=url, proxies=proxies, headers=headers, verify=verify)
        if method == 'OPTIONS':
            response = requests.options(url=url, proxies=proxies, headers=headers)
        if method == 'POST':
            response = requests.post(url=url, proxies=proxies, headers=headers, json=body, verify=verify)
        if method == 'PUT':
            response = requests.put(url=url, proxies=proxies, headers=headers, json=body, verify=verify)
        if method == 'PATCH':
            response = requests.patch(url=url, proxies=proxies, headers=headers, json=body, verify=verify)
        if method == 'DELETE':
            response = requests.delete(url=url, proxies=proxies, headers=headers, json=body, verify=verify)                    
        response_dict = APIMethods.generate_response_dict(method, url, params, body, headers, response)
        return response_dict

    @staticmethod
    def add_params_to_url(url, params):
        if params != '' and params != None:
            url = url + "?"
            for param_name, param_value in params.items():
                url = url + param_name + "=" + param_value + "&"
            url = url[:-1]
        return url
    
    @staticmethod
    def generate_response_dict(method, url, params, body, headers, response):
        response_dict = {
            "requestMethod": method,
            "requestURL": url,
            "requestParams": params,
            "requestBody": body,
            "requestHeaders": headers,
            "responseStatusCode": response.status_code
        }
        if response.text != None and response.text != "":
            response_dict["responseBody"] = json.loads(response.text)
        return response_dict

    #@staticmethod
    #def get_response(file_name):
    #    response = CM.read_json_file(f"Tests/filesForTests/temp_api/{file_name}")
    #    return response
    
    @staticmethod
    def get_path_of_json(path, json):
        if path == None or path == "":
            return json
        splitted_path = path.split(".")
        element = splitted_path[0]
        is_integer = False
        try:
            int(element)
            is_integer = True
        except Exception:
            pass
        if is_integer == True:
            temp_ele = json[int(element)]
        else:
            temp_ele = json[element]
        if len(splitted_path) == 1:
            return temp_ele
        else:
            del splitted_path[0]
            new_path = ".".join(splitted_path)
            return APIMethods.get_path_of_json(new_path, temp_ele)


    #This methods will filter the different elements in a list of elements and return THE FIRST element that matches the filter_element condition
    @staticmethod
    def get_correct_element_from_json_list(path_of_list_of_elements, response_body, filter_element):
        #response_body = APIMethods.get_json_from_file(file_name)
        elements = APIMethods.get_path_of_json(path_of_list_of_elements, response_body)
        for element in elements:
            correct_element = True
            if filter_element == None or filter_element == "":
                raise Exception("The filter element provided is empty")
            for filter_name, filter_value in filter_element.items():
                if filter_name not in element:
                    correct_element = False
                else:
                    if element[filter_name] != filter_value:
                        correct_element = False
            if correct_element == True:
                #now = datetime.now()
                #now_string = now.strftime("%Y%m%d%H%M%S%f")
                #file_name = f"json_element_{now_string}.json"
                #CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", element)
                #return file_name
                return element
        return ""
    
    @staticmethod
    def get_correct_elements_from_json_list(path, response_body, filter_element):
        #response_body = APIMethods.get_json_from_file(file_name)
        elements = APIMethods.get_path_of_json(path, response_body)
        new_list_of_elements = {"elements":[]}
        for element in elements:
            correct_element = True
            if filter_element == None or filter_element == "":
                raise Exception("The filter element provided is empty")
            for filter_name, filter_value in filter_element.items():
                if filter_name not in element:
                    correct_element = False
                else:
                    if element[filter_name] != filter_value:
                        correct_element = False
            if correct_element == True:
                new_list_of_elements["elements"].append(element)
        #now = datetime.now()
        #now_string = now.strftime("%Y%m%d%H%M%S%f")
        #file_name = f"json_element_{now_string}.json"
        #CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", new_list_of_elements)
        #return file_name
        return new_list_of_elements
    
    @staticmethod
    def assert_value_of_json(path, json, expected_result):
        #json = APIMethods.get_json_from_file(file_name)
        field = APIMethods.get_path_of_json(path, json)
        assert str(expected_result) == str(field)

    @staticmethod
    def get_json_from_file(file_name):
    #    if "json_element_" in file_name:
    #        json = CM.read_json_file(f"Tests/filesForTests/temp_api/{file_name}")
    #    if "api_response_" in file_name:
    #        json = CM.read_json_file(f"Tests/filesForTests/temp_api/{file_name}")["responseBody"]
        if "validation_json_" in file_name:
            json = CM.read_json_file(f"Tests/filesForTests/Data/{file_name}")
        return json
    
    #@staticmethod
    #def get_status_code_from_file(file_name):
    #    status_code = CM.read_json_file(f"Tests/filesForTests/temp_api/{file_name}")["responseStatusCode"]
    #    return status_code
    
    #@staticmethod
    #def assert_status_code(file_name, expected_status_code):
    #    status_code = APIMethods.get_status_code_from_file(file_name)
    #    assert str(status_code) == str(expected_status_code)
    
    @staticmethod
    def assert_json_in_another_json(json_body, expected_json_body):
        #json_body = APIMethods.get_json_from_file(file_name)
        #expected_json_body = APIMethods.get_json_from_file(expected_json_file_name)
        for key, value in expected_json_body.items():
            APIMethods._assert_element_in_json(key, value, json_body, expected_json_body)

    @staticmethod
    def _assert_element_in_json(element_name, element_value, json, expected_json_body):
        if element_name in json:
            if type(json[element_name]) is dict:
                for new_element_name, new_element_value in expected_json_body[element_name].items():
                    APIMethods._assert_element_in_json(new_element_name, new_element_value, json[element_name], expected_json_body[element_name])
            else:
                assert json[element_name] == element_value
        else:
            assert False

    #@staticmethod
    #def string_to_json_file(json_string):
    #    json = APIMethods.string_to_dict(json_string)
    #    now = datetime.now()
    #    now_string = now.strftime("%Y%m%d%H%M%S%f")
    #    file_name = f"json_element_{now_string}.json"
    #    CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", json)
    #    return file_name

    @staticmethod
    def dict_to_string(json_dict):
        json_string = json.dumps(json_dict)
        return json_string

    @staticmethod
    def assert_element_in_list_of_elements(path_of_list, json_body_with_list, json_body_to_assert):
        #json_body = APIMethods.get_json_from_file(file_name)
        #element_to_assert_json_body = APIMethods.get_json_from_file(element_to_assert_file_name)
        new_json_body = APIMethods.get_path_of_json(path_of_list, json_body_with_list)
        for element in new_json_body:
            correct_element = True
            for ele_key, ele_value in json_body_to_assert.items():
                if ele_key not in element:
                    correct_element = False
                    break
                else:
                    if element[ele_key] != ele_value:
                        correct_element = False
                        break
            if correct_element == True:
                return element
        assert False

    @staticmethod
    def assert_amount_of_records_in_list(path, file_name, amount):
        pass

    @staticmethod
    def assert_amount_of_records_in_list_more_than(path, file_name, amount):
        pass
    

        
    @staticmethod
    def repeat_api_request(retries,retry_until_status_code, method, url, params, body, headers, cookies, files, auth, timeout, allow_redirects, proxies, verify, stream, cert):
        count = 0
        retries = int(retries)
        retry_until_status_code = int(retry_until_status_code)
        while count != retries:
            count = count+1
            apiresponse = APIMethods.api_request(method, url, params, body, headers, cookies, files, auth, timeout, allow_redirects, proxies, verify, stream, cert)
            if(apiresponse['responseStatusCode'] == retry_until_status_code):
                break
        return apiresponse    
      
