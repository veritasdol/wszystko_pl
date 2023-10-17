from . import request

class Category:

    def get_all_categories(self, include_parameters: bool = False, page_size: int = 10, page:int = 1) -> dict:
        '''
        Returns the full list of categories along with all parameters, 
        their types, constraints, and dictionary values if include_parameters is True.\n
        arguments:
            include_parameters: bool,
            page_size: int; 10 <= x <= 100,
            page: int; x >= 1.
        '''
        
        params = {'includeParameters': include_parameters,
                  'pageSize': page_size,
                  'page': page}
        return request.send_request(method='GET', path='/categories', params=params)
    

    def get_category_info(self, category_id: int, parameters:bool = False, required_only: bool = False) -> dict:
        '''
        Returns the full information about category.
        If parameters is True, return category parameters.
        If required is True - return only required parameters only.\n
        arguments:
            category_id: int,
            parameters: bool,
            required_only: bool.
        '''

        if not parameters:
            return request.send_request(method='GET', path=f'/categories/{category_id}')
        elif parameters and not required_only:
            return request.send_request(method='GET', path=f'/categories/{category_id}/parameters')
        else:
            filtered_dict = self.__filter_category_params(request.send_request(
                method='GET', 
                path=f'/categories/{category_id}/parameters')
                )
            return filtered_dict

    
    def __filter_category_params(self, data: dict) -> dict:
        result_dict = {'fields':[]}
        for param in data['fields']:
            if param['required']:
                result_dict['fields'].append(param)
        return result_dict

    