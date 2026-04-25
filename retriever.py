def get_retriever(vectorstore, k = 5):
    return vectorstore.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k" : k}
    )