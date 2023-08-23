from django.db import connection
import timeit


def count_database_hits(func):
    def wrapper(*args, **kwargs):
        # Reset the connection's query count before executing the function
        connection.queries_log.clear()

        # Execute the function
        result = func(*args, **kwargs)

        # Get the number of queries executed
        num_queries = len(connection.queries)

        # Print or do something with the number of queries
        print(f"Number of database hits: {num_queries}")

        return result

    return wrapper

def count_database_hits_with_details(func):
    def wrapper(*args, **kwargs):
        # Reset the connection's query count before executing the function
        connection.queries_log.clear()

        # Execute the function
        result = func(*args, **kwargs)

        # Get the number of queries executed
        num_queries = len(connection.queries)

        # Print the number of queries
        print(f"Number of database hits: {num_queries}")

        # Print the details of each query
        for i, query in enumerate(connection.queries, start=1):
            print(f"Query {i}: {query['sql']}")

            # Check if the 'params' key exists in the query dictionary
            if 'params' in query:
                print(f"Parameters: {query['params']}")
            else:
                print("No parameters")

            print()

        return result

    return wrapper


    return wrapper



def time_it(func):
    def wrapper(*args, **kwargs):
        # Measure the execution time
        start_time = timeit.default_timer()

        # Execute the function
        result = func(*args, **kwargs)

        # Calculate the execution time
        end_time = timeit.default_timer()
        execution_time = end_time - start_time

        # Print or do something with the execution time
        print(f"Execution time: {execution_time} seconds")

        return result

    return wrapper
