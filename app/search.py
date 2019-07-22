from flask import current_app

#each function checks if app.elasticsearch is None
#if so, it will return without doing anything

#each function accepts the index name as an argument

#functions that add and remove
    #take SQLalchemy model as a second argument
    #add to index and searchable class added to the model 
    #to build the document that is inserted in the index

    #using the id value for the unique identifier

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    #ex.delete function remove from index -- deletes the document stored under
    #under the given id
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

def query_index(index, query, page, per_page):
    #take the index name, text to search for, pagination controls, so search results
    #can be paginated
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        #multi match can search across multiple fields -- * -- and look in all fields
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    #returns id elements for search results and the total number of results
    return ids, search['hits']['total']