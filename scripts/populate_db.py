import sqlite3, json
from  pathlib import Path 

def setup_problem_db(db_name = "../db.sqlite3"):
    conn = sqlite3.connect(db_name)
    return conn

def insert_problem(conn,Id, Name,Grade,moves,
                IsBenchmark,IsAssessmentProblem, Method,
                setup,firstname,lastname,setyear=2017,**kwargs):
    cmd1 = "INSERT INTO moonboard_problem (id, name, grade, benchmark,assessmentproblem,method,firstname,lastname,setyear) VALUES (?,?,?,?,?,?,?,?,?)"
    cmd2 = "INSERT INTO moonboard_problemmove (id, position, setup, isstart, isend, problem_id) VALUES (NULL,?,?,?,?,?)"

    c = conn.cursor()
    try:
        c.execute(cmd1,(Id, Name.strip(),Grade.strip(), IsBenchmark, 
        IsAssessmentProblem, Method, firstname.strip(),lastname.strip(),setyear))
    except Exception as e :
        conn.rollback()
        raise e
    else:
        print(f"New problem {Id}.")
        conn.commit()


# %%
conn = setup_problem_db()

# %%
# Downloaded problems from https://github.com/e-sr/moonboard/tree/master/problems/fetch
problem_path = Path("esr/problems/fetch/moonboard_problems_setup_master2017.json")


# %%
with problem_path.open("r+") as f:
    problems=json.load(f)


# %%
errors=[]
for Id, problem in problems.items():
    try:
        setup=problem["Holdsetup"]["Description"][-4:]
        moves = [[m['Description'],m["IsStart"], m["IsEnd"]] for m in problem['Moves']]
        insert_problem(conn, moves=moves,setup=setup,Id=Id, 
                        firstname= problem['Setter']['Firstname'], 
                        lastname= problem['Setter']['Lastname'], 
                        **problem
        )
    except:
        errors.append(Id)

print(errors)


# %%
conn.close()