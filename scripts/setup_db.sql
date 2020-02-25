
DROP TABLE IF EXISTS holds;
DROP TABLE IF EXISTS setter;
DROP TABLE IF EXISTS problemMoves;
DROP TABLE IF EXISTS problems;
--
CREATE TABLE holds(
    Position TEXT,
    Setup TEXT,
    HoldSet TEXT,
    Hold INTEGER,
    Orientation TEXT,
    PRIMARY KEY (Position,Setup)
    );
--
CREATE TABLE setter
(
    Firstname TEXT,
    Lastname TEXT,
    PRIMARY KEY (Firstname,Lastname)
);
--
CREATE TABLE moonboard_problem(
    Id INTEGER PRIMARY KEY,
    Name TEXT ,
    Grade TEXT,
    Benchmark INTEGER,
    AssessmentProblem INTEGER,
    Method TEXT,
    Firstname TEXT,
    Lastname TEXT,
    SetYear TEXT,
    NameForUrl TEXT,
    DateInserted TEXT,
    IsMaster INTEGER,
    Repeats INTEGER,
    HoldSetup TEXT,
    SetAngle TEXT,
    FOREIGN KEY (Firstname,Lastname) REFERENCES setter(Firstname,Lastname)
    );
--
CREATE TABLE moonboard_problemmove(
    Id INTEGER,
    Position TEXT,
    Setup TEXT,
    Setangle TEXT,
    IsStart INTEGER,
    Problem_Id INTEGER,
    IsEnd INTEGER,
    PRIMARY KEY (Problem_Id,Position,Setup),
    FOREIGN KEY (Problem_Id) REFERENCES problems (Id),
    FOREIGN KEY (Position,Setup) REFERENCES holds (Position,Setup)
    );
