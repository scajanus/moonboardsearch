#%%
import sqlite3, json
from  pathlib import Path
from pprint import pprint
def setup_problem_db(db_name = "../db.sqlite3", init_script_path = Path("setup_db.sql")):
    conn = sqlite3.connect(db_name)
    return conn


def setup_holds(conn, hold_setup=Path("HoldSetup.json")):
    cmd = "INSERT INTO moonboard_holds VALUES (NULL, ?,?,?,?,?)"
    c = conn.cursor()
    with hold_setup.open("r+") as f:
        holds = json.load(f)
    print("insert holds")
    for setup,v in holds.items():
        print(setup)
        for pos, detail in v.items():
            c.execute(cmd, (pos, setup, detail['HoldSet'],
                       detail["Hold"], detail["Orientation"]))
    conn.commit()
    print("insert holds OK")


def insert_problem(conn,Id, Name,Grade,moves,
                Benchmark,AssessmentProblem, Method,
                setup,firstname,lastname,setyear,NameForUrl,DateInserted,Master,
                Repeats, HoldSetup, setangle,**kwargs):
    cmd0 = "INSERT INTO setter (firstname, lastname) VALUES (?,?)"
    cmd1 = "INSERT INTO moonboard_problem (id, name, grade, benchmark, assessmentproblem, method, firstname, lastname, setyear, nameforurl, dateinserted, ismaster, repeats, holdsetup, setangle, rating) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cmd2 = "INSERT INTO moonboard_problemmove (id, position, setup, setangle, isstart, problem_id, isend) VALUES (?,?,?,?,?,?,?)"
    rating =  kwargs['rating']

    c = conn.cursor()
    try:
        c.execute(cmd0,(firstname,lastname))
    except:
        conn.rollback()
    else:
        print(f"New Setter {firstname} {lastname}.")

    try:
        c.execute(cmd1,(
            Id,
            Name.strip(),
            Grade.strip(),
            Benchmark,
            AssessmentProblem,
            Method,
            firstname.strip(),
            lastname.strip(),
            setyear,
            NameForUrl.strip(),
            DateInserted.strip(),
            Master,
            Repeats,
            HoldSetup.strip(),
            setangle,
            rating
            )
            )
    except Exception as e :
        conn.rollback()
        raise e
    else:
        try:
            for (moveid,position,start,stop) in moves:
                c.execute(cmd2,[moveid, position, setup, setangle, start, Id, stop])
        except Exception as e :
            conn.rollback()
            raise e
        else:
            print(f"New problem {Id}.")
            conn.commit()

if __name__=="__main__":
    conn = setup_problem_db()
    setup_holds(conn)
    problem_path = dict()
    problems = dict()
    problem_path['2016'] = Path("scrape/readhar/2016/problems.json")
    problem_path['2017'] = Path("scrape/readhar/2017/problems.json")
    problem_path['2019'] = Path("scrape/readhar/2019/problems.json")
    for year in ['2016','2017','2019']:

        with problem_path[year].open("r+") as f:
            for key, data  in json.load(f).items():
                problems[key] = data



    errors=[]
    for Id, problem in problems.items():
        Id = int(Id)
        problem.pop('Id')
        try:
            setup=problem["Holdsetup"]["Description"][-4:]
            moves = [[m['Id'],m['Description'],m["IsStart"], m["IsEnd"]] for m in problem['Moves']]
            HoldSetup = problem['Holdsetup']['Description']
            if problem.get('MoonBoardConfiguration'):
                BoardConfig = problem['MoonBoardConfiguration'].get('Description','')
            else:
                BoardConfig = None
            AssessmentProblem = problem['IsAssessmentProblem']
            Master = problem["IsMaster"]
            Benchmark = problem["IsBenchmark"]
            if BoardConfig:
                if '25' in BoardConfig:
                    setangle=25
                else:
                    setangle=40
            else:
                setangle=40


            insert_problem(conn, moves=moves,setup=setup,Id=Id,
                            firstname= problem['Setter']['Firstname'],
                            lastname= problem['Setter']['Lastname'],
                            setyear=setup,
                            setangle=setangle,
                            HoldSetup=HoldSetup,
                            Master=Master,
                            Benchmark=Benchmark,
                            AssessmentProblem=AssessmentProblem,
                            rating=problem['UserRating'],
                            **problem
            )
        except sqlite3.Error as e:
            pprint(e)
            errors.append(Id)

    print(errors)
