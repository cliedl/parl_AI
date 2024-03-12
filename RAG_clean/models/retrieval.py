
def retriever(db, search_type="similarity", k=10):
    retriever = db.as_retriever(
        search_type=search_type,
        search_kwargs={
            "k": k,
            # "where": {  # https://docs.trychroma.com/usage-guide#using-where-filters
            #     "source": "" # TODO: add an exact file name here for testing purposes
            # },
        },
    )

    return retriever
