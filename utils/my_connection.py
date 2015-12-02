__author__ = 'sunary'
# chau.tran
# Clarify and organize functions 
__version__ = '1.1'        


def da0_connection(database='da0', user='dbw', password='sentifi.da0', 
                    host='da0.eu-west-1.compute.internal'):
    """
        Default is dbw user, no dbr user
    """
    import psycopg2
    try:
        return psycopg2.connect(database=database, user=user, password=password, 
                                host=host)
    except psycopg2.Error as er:
        print er


def dev_connection(database='nhat',user='dbr',password='sentifi', 
                    host='psql-dev-1.ireland.sentifi.internal'):
    """
        Default is dbr user
        SHOULD use dbr to query from database
               use dbw to update to database 
        When calling this function, SHOULD specify at least DATABASE and USER        
    """
    import psycopg2

    try:
        return psycopg2.connect(database=database, user=user, password=password, 
                                host=host)
    except pycopg2.Error as er:
        print er


def psql0_connection(database='rest_in_peace', user='dbr',password='sentifi', 
                    host='psql0.eu-west-1.compute.internal'):
    """
        Default is dbr user
        SHOULD use dbr to query from database
               use dbw to update to database 
        When calling this function, SHOULD specify at least DATABASE and USER        
    """
    import psycopg2

    try:
        return psycopg2.connect(database=database, user=user, password=password, 
                                host=host)
    except psycopg2.Error as er:
        print er


def psql1_connection(database='rest_in_peace', user='dbr', password='sentifi', 
                    host='psql1.eu-west-1.compute.internal'):
    """
        Default is dbr user
        SHOULD use dbr to query from database
               use dbw to update to database 
        When calling this function, SHOULD specify at least DATABASE and USER        
    """
    import psycopg2

    try:
        return psycopg2.connect(database=database, user=user, password=password, 
                                host=host)
    except psycopg2.Error as er:
        print er


def ellytran_connection(database='rip_slave1', user='dbr', password='sentifi', 
                    host='ellytran.eu-west-1.compute.internal', port=6432):
    """
        Default is dbr user, rip_slave1 database, port 6432
        SHOULD use dbr to query from database
               use dbw to update to database 
        When calling this function, SHOULD specify at least DATABASE and USER        
               
    """
    import psycopg2
    
    try:
        return psycopg2.connect(database=database, user=user, password=password, 
                                host=host, port=port)
    except Error as er:
        print er
#     return psycopg2.connect(database=database, user='dbw', password='sentifi',
#                             host='ellytran.eu-west-1.compute.internal', port=6432)


# def ellytran_write_connection(database='rip_master'):
#     import psycopg2
# 
#     return psycopg2.connect(database=database, user='dbw', password='sentifi',
#                             host='ellytran.eu-west-1.compute.internal', port=6432)


def es_connection():
    from elasticsearch import Elasticsearch
    try:
        return Elasticsearch(
            hosts=['es0.eu-west-1.compute.internal',
               'es4.eu-west-1.compute.internal',
               'es5.eu-west-1.compute.internal',
               'es8.eu-west-1.compute.internal',
               'es9.eu-west-1.compute.internal'],
            retry_on_timeout=True,
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniff_timeout=3600,
            timeout=3600,
        )
    except Error as er:
        print er

def cassandra_cluster():
    from cassandra.cluster import Cluster
    from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy, RetryPolicy

    cassandra_hosts = [
        '10.0.0.251',
        '10.0.0.250',
        '10.0.0.249']
    try:
        return Cluster(
            contact_points=cassandra_hosts,
            load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy(local_dc='Cassandra')),
            default_retry_policy=RetryPolicy()
        )
    except Error as er:
        print er
