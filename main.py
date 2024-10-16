from swarm import Agent
from swarm.repl import run_demo_loop
import psycopg2

STARTER_PROMPT = """You are an intelligent and technically skilled SQL engineer who responds to requests for data.

You may ask clarifying questions about the user's intent which allow you to construct a correct SQL query.

When you understand the user request, generate a valid SQL select statement and execute it against the database.

If the generated SQL has any order by clauses using aggregate functions, alias the aggregate function and use the alias in the order by clause instead.

You have access to the database INFORMATION_SCHEMA.columns output, provided below:

[('s_comment', ':utf8', 'xtdb', 'supplier', 'public'),
 ('s_phone', ':utf8', 'xtdb', 'supplier', 'public'),
 ('s_nationkey', ':utf8', 'xtdb', 'supplier', 'public'),
 ('_id', ':utf8', 'xtdb', 'supplier', 'public'),
 ('s_name', ':utf8', 'xtdb', 'supplier', 'public'),
 ('s_address', ':utf8', 'xtdb', 'supplier', 'public'),
 ('s_acctbal', ':f64', 'xtdb', 'supplier', 'public'),
 ('s_suppkey', ':utf8', 'xtdb', 'supplier', 'public'),
 ('r_regionkey', ':utf8', 'xtdb', 'region', 'public'),
 ('_id', ':utf8', 'xtdb', 'region', 'public'),
 ('r_comment', ':utf8', 'xtdb', 'region', 'public'),
 ('r_name', ':utf8', 'xtdb', 'region', 'public'),
 ('n_comment', ':utf8', 'xtdb', 'nation', 'public'),
 ('n_nationkey', ':utf8', 'xtdb', 'nation', 'public'),
 ('_id', ':utf8', 'xtdb', 'nation', 'public'),
 ('n_regionkey', ':utf8', 'xtdb', 'nation', 'public'),
 ('n_name', ':utf8', 'xtdb', 'nation', 'public'),
 ('c_mktsegment', ':utf8', 'xtdb', 'customer', 'public'),
 ('c_acctbal', ':f64', 'xtdb', 'customer', 'public'),
 ('c_nationkey', ':utf8', 'xtdb', 'customer', 'public'),
 ('c_comment', ':utf8', 'xtdb', 'customer', 'public'),
 ('c_name', ':utf8', 'xtdb', 'customer', 'public'),
 ('c_phone', ':utf8', 'xtdb', 'customer', 'public'),
 ('_id', ':utf8', 'xtdb', 'customer', 'public'),
 ('c_address', ':utf8', 'xtdb', 'customer', 'public'),
 ('c_custkey', ':utf8', 'xtdb', 'customer', 'public'),
 ('o_totalprice', ':f64', 'xtdb', 'orders', 'public'),
 ('o_orderkey', ':utf8', 'xtdb', 'orders', 'public'),
 ('o_shippriority', ':i64', 'xtdb', 'orders', 'public'),
 ('o_orderstatus', ':utf8', 'xtdb', 'orders', 'public'),
 ('o_clerk', ':utf8', 'xtdb', 'orders', 'public'),
 ('o_orderpriority', ':utf8', 'xtdb', 'orders', 'public'),
 ('_id', ':utf8', 'xtdb', 'orders', 'public'),
 ('o_custkey', ':utf8', 'xtdb', 'orders', 'public'),
 ('o_comment', ':utf8', 'xtdb', 'orders', 'public'),
 ('o_orderdate', '[:date :day]', 'xtdb', 'orders', 'public'),
 ('ps_suppkey', ':utf8', 'xtdb', 'partsupp', 'public'),
 ('ps_availqty', ':i64', 'xtdb', 'partsupp', 'public'),
 ('ps_comment', ':utf8', 'xtdb', 'partsupp', 'public'),
 ('ps_partkey', ':utf8', 'xtdb', 'partsupp', 'public'),
 ('ps_supplycost', ':f64', 'xtdb', 'partsupp', 'public'),
 ('_id', ':utf8', 'xtdb', 'partsupp', 'public'),
 ('l_suppkey', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_shipdate', '[:date :day]', 'xtdb', 'lineitem', 'public'),
 ('l_tax', ':f64', 'xtdb', 'lineitem', 'public'),
 ('l_orderkey', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_receiptdate', '[:date :day]', 'xtdb', 'lineitem', 'public'),
 ('l_partkey', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_extendedprice', ':f64', 'xtdb', 'lineitem', 'public'),
 ('l_quantity', ':f64', 'xtdb', 'lineitem', 'public'),
 ('l_discount', ':f64', 'xtdb', 'lineitem', 'public'),
 ('l_returnflag', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_comment', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('_id', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_linestatus', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_shipinstruct', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_shipmode', ':utf8', 'xtdb', 'lineitem', 'public'),
 ('l_linenumber', ':i64', 'xtdb', 'lineitem', 'public'),
 ('l_commitdate', '[:date :day]', 'xtdb', 'lineitem', 'public'),
 ('p_mfgr', ':utf8', 'xtdb', 'part', 'public'),
 ('p_comment', ':utf8', 'xtdb', 'part', 'public'),
 ('p_size', ':i64', 'xtdb', 'part', 'public'),
 ('p_brand', ':utf8', 'xtdb', 'part', 'public'),
 ('p_retailprice', ':f64', 'xtdb', 'part', 'public'),
 ('_id', ':utf8', 'xtdb', 'part', 'public'),
 ('p_name', ':utf8', 'xtdb', 'part', 'public'),
 ('p_partkey', ':utf8', 'xtdb', 'part', 'public'),
 ('p_container', ':utf8', 'xtdb', 'part', 'public'),
 ('p_type', ':utf8', 'xtdb', 'part', 'public'),
 ('system_time', '[:timestamp-tz :micro "UTC"]', 'xtdb', 'txs', 'xt'),
 ('committed', ':bool', 'xtdb', 'txs', 'xt'),
 ('_id', ':i64', 'xtdb', 'txs', 'xt'),
 ('error', '[:union #{:null :transit}]', 'xtdb', 'txs', 'xt')]
"""


def exec_select_query(query):
    """Executes the provided SQL SELECT query against the read-only database"""
    print(f"SQL: \033[32;1m{query}\033[0m")
    conn = psycopg2.connect(database = "xtdb",
                            host= 'localhost',
                            port = 5432)
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


sql_agent = Agent(
    name = "SQL Agent",
    instructions = STARTER_PROMPT,
    functions = [exec_select_query],
)

if __name__ == "__main__":
    run_demo_loop(sql_agent, stream=True)
