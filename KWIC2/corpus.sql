CREATE TABLE corpus (
    corpusid TEXT PRIMARY KEY,
    nowords INTEGER,
    docount INTEGER
);
CREATE TABLE document (
    documentid TEXT PRIMARY KEY,
    corpusid TEXT,
    filepath TEXT,
    nowords INTEGER,
    summary TEXT,
    wordbag TEXT,
    FOREIGN KEY (corpusid)
        REFERENCES corpus (corpusid)
);
CREATE TABLE textline (
    lineid TEXT PRIMARY KEY,
    documentid TEXT NOT NULL,
    lineno INTEGER,
    linetext TEXT,
    possent REAL,
    nuesent REAL,
    negsent REAL,
    compsent REAL,
    FOREIGN KEY (documentid)
        REFERENCES document (documentid)
);
CREATE TABLE entity (
    entityname TEXT NOT NULL PRIMARY KEY,
    variants TEXT
);
Create TABLE context (
    contextid TEXT PRIMARY KEY,
    entityid TEXT NOT NULL,
    lineid TEXT NOT NULL,
    FOREIGN KEY (entityid)
        REFERENCES entity (entityid),
    FOREIGN KEY (lineid)
        REFERENCES textline (lineid)
);
Create TABLE similiaty (
    simmilarityid INTEGER PRIMARY KEY,
    similitary REAL,
    sourceid TEXT,
    targetid TEXT,
    FOREIGN KEY (sourceid)
        REFERENCES document (documentid),
    FOREIGN KEY (sourceid)
        REFERENCES document (documentid)
);
